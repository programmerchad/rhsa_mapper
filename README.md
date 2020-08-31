<!-- PROJECT SHIELDS -->
[![Python][python-shield]][python-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- ABOUT THE PROJECT -->
## rhsa_mapper

### About this project
Built out of a necessity to quickly determine what Red Hat repositories a set of Red Hat Security Advisories belong to, the RHSA Mapper allows the user to quickly identify what CPEs and repositories are impacted by a RHSAs.

Features:
* Map CPEs from OVAL Files to repositories.
* Retrieve a list of all CPEs available in the `repository-to-cpe.json` mapping provided by [Red Hat](https://www.redhat.com/security/data/metrics/repository-to-cpe.json).
* Retrieve a list of repositories containing a given CPE(s).
* Retrieve a list of all repositories available in the `repository-to-cpe.json` mapping provided by [Red Hat](https://www.redhat.com/security/data/metrics/repository-to-cpe.json).
* Retrieve a list of CPEs found in a given repository/repositories.

## Prerequisites

If you plan to use the `advisory search` command, you will need to have an [OVAL file](https://www.redhat.com/security/data/oval/v2) saved and extracted locally.

<!-- USAGE EXAMPLES -->
## Installation and General Use

To get started, clone this repository and install the package:
```sh
$ git clone https://github.com/programmerchad/rhsa_mapper.git
$ cd rhsa_mapper/
$ pip install .
```

Once installed, you can use the package with the `rhsam` command:
```sh
$ rhsam --help
Usage: rhsam [OPTIONS] COMMAND [ARGS]...

  Red Hat Mapper - Several useful utilities for retrieving CPE/Repository
  mappings for Red Hat.

Options:
  --help  Show this message and exit.

Commands:
  advisory  Commands to be used with advisory_search
  cpe       Commands to be used with cpes
  repo      Commands to be used with repos
```

Retrieve a list of all CPEs found in the `repository-to-cpe.json` mapping provided by [Red Hat](https://www.redhat.com/security/data/metrics/repository-to-cpe.json):
```sh
$ rhsam cpe list --save -d ~/Downloads -o rhsam_cpes.json
Gathering list of CPEs...
599 CPEs found...
  - cpe:/a:redhat:3scale_amp:2.8::el8
  - cpe:/a:redhat:3scale_amp:2.9::el8
  - cpe:/a:redhat:a_mq_clients:1::el5
  ...snip...
```

Retrieve a list of Red Hat repositories that contain a given CPE(s):
```sh
$ rhsam cpe search cpe:/a:redhat:openshift:4.5::el8 cpe:/a:redhat:rhel_satellite_tools:8
Gathering a list of repositories that contain cpe:/a:redhat:openshift:4.5::el8 or cpe:/a:redhat:rhel_satellite_tools:8...
Found 9 repositories containing cpe:/a:redhat:openshift:4.5::el8 or cpe:/a:redhat:rhel_satellite_tools:8...
  - rhocp-4.5-for-rhel-8-ppc64le-debug-rpms
  - rhocp-4.5-for-rhel-8-ppc64le-rpms
  ...snip...
Found 108 repositories containing cpe:/a:redhat:openshift:4.5::el8 or cpe:/a:redhat:rhel_satellite_tools:8...
  - satellite-tools-6.5-for-rhel-8-aarch64-debug-rpms
  - satellite-tools-6.5-for-rhel-8-aarch64-eus-debug-rpms
```

Retrieve a list of all repositories found in the `repository-to-cpe.json` mapping provided by [Red Hat](https://www.redhat.com/security/data/metrics/repository-to-cpe.json):
```sh
$ rhsam repo list --save -d ~/Downloads -o rhsam_repo.json
Gathering list of repositories...
3523 repositories found...
Saving repository list to /Users/cdombrowski/Downloads/rhsam_repo.json
  - 3scale-amp-2-rpms-for-rhel-8-x86_64-debug-rpms
  - 3scale-amp-2-rpms-for-rhel-8-x86_64-rpms
  - 3scale-amp-2-rpms-for-rhel-8-x86_64-source-rpms
  ...snip...
```

Retrieve a list of CPEs that appear in a given repository/repositories:
```sh
$ rhsam cpe search cpe:/a:redhat:openshift:4.5::el8 cpe:/a:redhat:rhel_satellite_tools:8
Gathering a list of repositories that contain cpe:/a:redhat:openshift:4.5::el8 or cpe:/a:redhat:rhel_satellite_tools:8...
Found 9 repositories containing cpe:/a:redhat:openshift:4.5::el8 or cpe:/a:redhat:rhel_satellite_tools:8...
  - rhocp-4.5-for-rhel-8-ppc64le-debug-rpms
  - rhocp-4.5-for-rhel-8-ppc64le-rpms
  ...snip...
Found 108 repositories containing cpe:/a:redhat:openshift:4.5::el8 or cpe:/a:redhat:rhel_satellite_tools:8...
  - satellite-tools-6.5-for-rhel-8-aarch64-debug-rpms
  - satellite-tools-6.5-for-rhel-8-aarch64-eus-debug-rpms
```

Search for advisories in the local `rhel-8.oval.xml` file in the `C:\Users\chad\Downloads` directory and save the output to the provided filename (`rhsam.json`):

```sh
$ rhsam advisory parse rhel-8.oval.xml ~/Downloads --save -o rhsam.json -d ~/Downloads
Processing /Users/chad/Downloads/rhel-8.oval.xml:   [###---------------------------------]    9%  00:01:14
```

Searching for a specific advisory in the local `rhel-8.oval.xml` file:
```sh
$ rhsam advisory search RHSA-2019:0966 rhel-8.oval.xml ~/Downloads -d ~/Downloads/ -o rhsam_advisory.json --save
Searching for RHSA-2019:0966 in /Users/chad/Downloads/rhel-8.oval.xml...
RHSA-2019:0966 found in /Users/chad/Downloads/rhel-8.oval.xml...
Advisory RHSA-2019:0966:
  Contains 2 CPEs...
    - cpe:/a:redhat:enterprise_linux:8
    - cpe:/a:redhat:enterprise_linux:8::appstream
  Applies to 36 repositories...
    - rhel-8-for-aarch64-appstream-debug-rpms
    - rhel-8-for-aarch64-appstream-eus-debug-rpms
    ...snip...
```

<!-- CONTRIBUTING -->
## Contributing

Feel free to contribute to this project to add any features or improvements that you'd like.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/newFeature`)
3. Commit your Changes (`git commit -m 'Add some new feature'`)
4. Push to the Branch (`git push origin feature/newFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Chad Dombrowski - [@programmerchad](https://twitter.com/programmerchad) - [cdombrowski85@gmail.com](mailto:cdombrowski85@gmail.com?subject=[GitHub]%20RHSA%20Mapper)

Project Link: [https://github.com/programmerchad/rhsa_mapper](https://github.com/programmerchad/rhsa_mapper)


<!-- MARKDOWN LINKS & IMAGES -->
[python-shield]: https://img.shields.io/badge/python-3.8-blue.svg?style=flat-square
[python-url]: https://www.python.org/
[contributors-shield]: https://img.shields.io/github/contributors/programmerchad/rhsa_mapper?style=flat-square
[contributors-url]: https://github.com/programmerchad/rhsa_mapper/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/programmerchad/rhsa_mapper?style=flat-square
[forks-url]: https://github.com/programmerchad/rhsa_mapper/network/members
[stars-shield]: https://img.shields.io/github/stars/programmerchad/rhsa_mapper?style=flat-square
[stars-url]: https://github.com/programmerchad/rhsa_mapper/stargazers
[issues-shield]: https://img.shields.io/github/issues/programmerchad/rhsa_mapper?style=flat-square
[issues-url]: https://github.com/programmerchad/rhsa_mapper/issues
[license-shield]: https://img.shields.io/github/license/programmerchad/rhsa_mapper?style=flat-square
[license-url]: https://github.com/programmerchad/rhsa_mapper/blob/master/LICENSE.txt
