# shaksz
All coding and design solutions as package


# Unit Tests
`python -m unittest discover -s tests`

# Build package


    python setup.py sdist bdist_wheel



# Publish Test

    twine upload --repository testpypi dist/*

# Publish Prod
    TBD

    pip install twine

    twine upload dist/*


# Consumption
    import shaksz

    result = shaksz.leetcode.twoSum([2, 7, 11, 15], 9)

    print(result)
