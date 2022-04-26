# Changelog

## 3.0.0 - 2022-04-26

- Move to Python 3.7+ only
- Add support for querying via TCP
- Move to DNS Python dns.resolver.resolve from dns.resolver.query [#10](https://github.com/gmr/srvlookup/pull/10) - ([shizacat](https://github.com/shizacat))
- Move to GitHub actions from Travis CI
- Refactor to Python package from Python module
- Add Type annotations

## 2.0.0 - 2018-01-30

- Drop support for Python 2.6
- Include hostname in SRV tuple [#5](https://github.com/gmr/srvlookup/pull/5) - ([optiz0r](https://github.com/optiz0r))

## 1.0.0 - 2016-10-28

- Stable release
- Add sorting by weight and priority instead of only by priority

## 0.2.0 - 2015-06-08

- Look up SRV names in DNS additional records segment

## 0.1.0 - 2014-03-11

Initial Version
