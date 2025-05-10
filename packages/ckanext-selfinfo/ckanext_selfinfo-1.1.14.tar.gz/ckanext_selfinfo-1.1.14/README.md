# ckanext-selfinfo

This extension is built to represent a basic information about the running CKAN Application accessible only to admins.

CKAN should be configured to be able to connect to Redis as it heavily relies on it for storage.

On CKAN admin page `/ckan-admin/selfinfo` can see a big variety of information such as System Info, RAM, disk Usage, CKAN Errors, GIT Info and more.

![Main Selfinfo Screen](docs/assets/main_screen.png)

Check full [documentation](https://datashades.github.io/ckanext-selfinfo/) for more information.

## Requirements

Compatibility with core CKAN versions:

  | CKAN version | Compatibility                           |
  |--------------|-----------------------------------------|
  | 2.7          | untested                                |
  | 2.8          | untested                                |
  | 2.9          | untested                                |
  | 2.10         | yes                                     |
  | 2.11         | yes                                     |
  | master       | yes as of 2025/05 (check test results)  |


## License

MIT
