# Embedding service

Keeps SigLIP 2 resident so the dashcam backend can turn a search prompt into a
vector without paying model load time per request. CPU only.

Companion to `../VECTOR_SEARCH_RUNBOOK.md`, which covers the search itself.

## Run it locally

```bash
python -m venv venv
. venv/bin/activate                 # Windows: venv\Scripts\activate

# CPU torch FIRST -- see the note in requirements.txt. On Linux, plain
# `pip install torch` pulls the CUDA build: ~2.5 GB this service never uses.
# On Windows the default wheel is already CPU-only, so the index-url is
# harmless there but required on Linux.
pip install --index-url https://download.pytorch.org/whl/cpu torch
pip install -r requirements.txt

copy .env.example .env              # Linux/macOS: cp
```

Edit `.env` if needed. The default `MODEL_PATH` is a **relative path that
resolves against this folder**, so with the workspace layout intact it already
points at the checkpoint:

```
MODEL_PATH=../visibility_classifier/models/siglip2-so400m-patch16-512
```

Absolute paths are used verbatim; a bare HF repo id is passed through to
transformers. Both `.env` and relative `MODEL_PATH` resolve against this
directory rather than the working directory, so `uvicorn app:app` behaves the
same wherever it is launched from. Nothing needs exporting — the service loads
`.env` itself.

```bash
uvicorn app:app --host 127.0.0.1 --port 8100
# add --reload while you are editing
```

Startup loads several GB of weights; expect tens of seconds before it
answers. `/health` reports `load_seconds` once it is up.

Then, from another shell:

```bash
python smoke_test.py
```

That checks the things that fail silently: dimension, unit-norm vectors, cache
behaviour, and that repeated prompts give byte-identical vectors. It also prints
your **uncached single-prompt latency**, which is the number that decides how
hard you need to cache.

## API

`POST /embed`

```json
{ "texts": ["a dashcam photo of a road work zone"],
  "format": "pgvector",
  "mean": false }
```

- `format: "pgvector"` returns `"[0.1,-0.2,...]"` strings, ready to bind
  straight into the search query. Saves the backend formatting floats.
- `mean: true` averages all texts into one re-normalized vector — what
  `concept.kind = 'text'` does for a multi-prompt concept.

`GET /health` reports `model_name`, `dim`, threads, load time, and cache stats.

`POST /cache/clear` empties the prompt cache.

## Calling it from the backend

```python
import requests

r = requests.post("http://embedding:8100/embed",
                  json={"texts": [prompt], "format": "pgvector"}, timeout=30)
literal = r.json()["vectors"][0]
# then bind `literal` as :q in the two-stage search query
```

**Assert the model matches at startup.** The service and the index must agree on
the checkpoint, or you get plausible, wrong results — the same silent-failure
family as everything else in this system:

```python
health = requests.get("http://embedding:8100/health").json()
assert health["dim"] == 1152
assert health["model_name"] == <model_name from your embed_model row>
```

Note the ingest script recorded a local path in `embed_model`, e.g.
`models\siglip2-so400m-patch16-512`, not the HF id. Set `MODEL_NAME` to whatever
that row actually says.

## Docker

The checkpoint is neither committed nor baked into the image. `fetch_model.sh`
pulls a zip of the model folder from Object Storage into the mounted volume on
first start, and is a no-op on every start after that.

The image is defined by `../embedding_dockerfile` (top level of the backend
repo) and builds from the parent of the repo, so the frontend and backend
images share one context. Deploys go through `docker compose`; to build it
standalone from this directory:

```bash
docker build -f ../embedding_dockerfile -t dashcam-embed ../..

docker volume create dashcam-models     # once

docker run -p 8100:8100 \
  -v dashcam-models:/models \
  -e MODEL_PAR_URL='https://objectstorage.us-ashburn-1.oraclecloud.com/p/<token>/n/idnz0hftfltw/b/dashcam_models/o/' \
  -e MODEL_NAME='models\siglip2-so400m-patch16-512' \
  -e TORCH_THREADS=4 \
  dashcam-embed
```

First start downloads ~4.2 GB before the model loads, so give it a few minutes
and watch for `[fetch_model] checkpoint ready`. Later starts skip straight to
loading.

**Why not bake the weights into the image.** It would take the image from ~1 GB
to ~4.5 GB, re-download on every `--no-cache` build, and — because a PAR is a
bearer credential — write that URL permanently into `docker history`. Keep the
PAR in the runtime environment only.

**PAR or the oci CLI?** Set `MODEL_PAR_URL` and the fetch is one `curl` with no
CLI and no auth config; the cost is a credential to rotate before it expires.
Leave it unset on an OCI host that has the `oci` CLI and the script falls back
to `oci os object get --auth instance_principal` — no secret, no expiry — which
is the better option wherever it is available.

### Staging on the host instead

To avoid putting a PAR in the container environment at all, run the same script
on the host and mount the result read-only:

```bash
sudo MODEL_PATH=/opt/models/siglip2-so400m-patch16-512 \
     MODEL_PAR_URL='https://...' \
     ./fetch_model.sh

docker run -p 8100:8100 \
  -v /opt/models:/models:ro \
  -e FETCH_MODEL=never \
  ... dashcam-embed
```

`fetch_model.sh` needs ~8.6 GB of free disk while it works (the zip plus the
extracted tree; the zip is deleted as soon as it is unpacked) and leaves ~4.4 GB.
It writes `MODEL_PATH` only after a successful extract, so an interrupted fetch
never leaves a half-written folder that the next run mistakes for valid.

### Updating the checkpoint

Changing the model means re-embedding every row in `image_vector` and rebuilding
`siglip_median_m1()` and the index — see `../migrations/add_vector_tables.sql`.
For the same checkpoint re-fetched (corrupt copy, say), delete the folder in the
volume and restart the container.

## Sizing and tuning

- **One uvicorn worker, on purpose.** The model is several GB resident and a
  forward pass is already multi-threaded. A second worker doubles memory to
  serve requests that contend for the same cores. Scale `TORCH_THREADS`, not
  workers.
- **Inference is serialized behind a lock.** Letting N concurrent requests each
  spawn `TORCH_THREADS` threads thrashes rather than scales. This keeps latency
  predictable.
- **`TORCH_THREADS=4`** is a starting point on the 8 OCPU / 16 vCPU app server.
  The web app shares those cores; don't take all of them.
- **Cache aggressively.** Search prompts repeat heavily, and a hit turns
  hundreds of milliseconds into microseconds. The natural next step is
  precomputing common searches into `concept` rows, at which point the service
  isn't consulted for them at all.
- **`LOAD_VISION=false` by default.** Query-by-example over frames already in
  `image_vector` does not need the vision tower — those vectors are stored, and
  averaging them is pure SQL (`l2_normalize(avg(embedding))`). Only
  user-uploaded images need it. Turning it on roughly doubles resident memory
  and load time.

## Gotchas

- **Tokenization must stay `padding="max_length"`.** SigLIP is trained with
  fixed-length padded text. Default padding silently produces different
  embeddings that will not match the vectors in `image_vector`.
- **`HF_HUB_OFFLINE=1`** is set in the Dockerfile. If transformers reports a
  connection error, the local model folder wasn't found and it fell back to
  treating the path as a Hub repo id.
- Vectors come back **L2-normalized fp32**. The `similarity` returned by the
  search query is cosine; convert to a SigLIP probability app-side with
  `sigmoid(similarity * logit_scale + logit_bias)` using the constants from
  `/health`.
