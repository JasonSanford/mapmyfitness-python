## Validation

PEP8 validation (--ignore==E501, line length) is strictly enforced

## Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too:

    nosetests --with-coverage --cover-package mapmyfitness

View coverage:

    coverage html
