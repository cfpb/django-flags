workflow "Publish" {
  on = "release"
  resolves = ["Publish to PyPI"]
}

action "Publish to PyPI" {
  uses = "cfpb/pypi-publish-action@master"
  secrets = ["TWINE_USERNAME", "TWINE_PASSWORD"]
  env = {
    LIVE_PYPI = "True"
  }
}
