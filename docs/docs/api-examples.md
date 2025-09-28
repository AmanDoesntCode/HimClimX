# API Examples

```bash
curl http://127.0.0.1:8000/meta/variables
curl http://127.0.0.1:8000/meta/regions

curl -X POST http://127.0.0.1:8000/analyze \
  -H 'content-type: application/json' \
  -d '{"variable_id":"tavg","region_id":"L1","time_range":{"start":"2023-01-01","end":"2024-12-31"},"options":["trend","quality"]}'

curl -X POST http://127.0.0.1:8000/forecast \
  -H 'content-type: application/json' \
  -d '{"variable_id":"tavg","region_id":"L1","horizon_years":3}'

