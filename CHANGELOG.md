# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [0.6.0] - 2022-01-31

### Added
- New annotator to explore images in a directory (`ExploreAnnotator`).
- New annotator for video format (`VideoAnnotator`).
- New tutorial showing how to use the video annotator.
- New artifical data generator for video.
- New linter to ensure code standard.

### Changed
- Updated the CI/CD to add the linter verification.
- Started to switch classes from Pydantic models to use Attrs.
- Refactored callbacks to use the standard `on_<prefix>_<action>` ex. `on_navi_clicked`.
- Updated dataset download to use `pooch`.

## [0.5.2] - 2022-01-01

### Added

- New state layer to decouple individual annotators using [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation and [PyPubSub](https://pypi.org/project/PyPubSub/) for comunication.
- New tutorial showing how to build annotators by [Ítalo Epifânio](https://github.com/itepifanio).
- New debug module for annotators by [Carlos Cerqueira](https://github.com/Carloscerq).
- New voila dockerfile by [Carlos Cerqueira](https://github.com/Carloscerq).

### Changed

- Refactored the annotators to use the new state layer by [Ítalo Epifânio](https://github.com/itepifanio).
- Allow users to draw multiple bboxes on the BBoxAnnotator by [Enrique Moran](https://github.com/EnriqueMoran) with [its PR](https://github.com/palaimon/ipyannotator/pull/11) (adapted by [Ítalo Epifânio](https://github.com/itepifanio)).
- Revisited the tutorial API by [Alexander Pisarenko](https://github.com/AlexJoz).
- Documentation enhancements and updates to use nbdev to build it by [Carlos Cerqueira](https://github.com/Carloscerq).

### Fixed

- CI test check_lib_diff not validating all notebooks by [Carlos Cerqueira](https://github.com/Carloscerq).
