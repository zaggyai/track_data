# track_data
Motorsports track data aggregated from multiple sources on the interwebz.

## Schema

The data is stored in JSON files, one file per track definition.  There might be some duplication depending on ages of circuits or alternate layouts used, so use with caution.

Sample from `263503b671d694ae2dd1d7892d9e195a--road-atlanta.json`

```
{
    "name": "Road Atlanta",
    "short_name": "RA Moto GP",
    "start_finish": {
        "lat": 341504171,
        "lon": -838141874,
        "elev": 298000
    },
    "pts": [
        {
            "lat": 341504171,
            "lon": -838141874,
            "elev": 298000
        },
        ...
    ]
}
```

Note that GPS lat/lon values are encoded as integers to maintain precision; multiply by `1.0e-07` to get actual coords.
Also note that elevation is measured in millimeters.

## Contributing

If you find missing or erroneous data, please feel free to open an issue and/or create a pull request with the corrections or new tracks.

## License

Released under the highly-permissive MIT License - which also absolves us of warranty or liability.  Use at your own risk; ymmv, _etc ad nauseum_.
