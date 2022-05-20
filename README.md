An API for processing data against an ML model

## install

`pip install -r requirements.txt`

### set up
To initialise logging work 
`run build_scripts/build.sh`


## endpoints
### /posts/
Post must contain `paragraphs` key, otherwise will 400

## tests
`python -m unittest`

## notes
No data is returned from the server since there is an assumed db interface that hasn't been mocked here.
