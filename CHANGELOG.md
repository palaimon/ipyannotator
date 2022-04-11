# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [0.8.1] - 2022-04-09

### Changed
- Refactored notebooks to use python to handle folder structure instead of linux commands by [Ítalo Epifânio](https://github.com/itepifanio).

### Added
- [tqdm](itlab.palaimon.io/products/ipyannotator/ipyannotator/-/merge_requests) dependency [Ítalo Epifânio](https://github.com/itepifanio).
- Doc section explaining Ipyannotator dev dependencies [Ítalo Epifânio](https://github.com/itepifanio).

## [0.8.0] - 2022-04-09

### Changed
- Make the creation of new label classes more flexible and decouple it from the folder structure by [Ítalo Epifânio](https://github.com/itepifanio).
- Refactored Im2Im and Capture annotators to render any widget on grid menu by [Ítalo Epifânio](https://github.com/itepifanio).
- Replaced exception with warning when using the same file storage on multiple annotators by [Ítalo Epifânio](https://github.com/itepifanio).

### Added
- New `fit_canvas` option to adjust images to the size of the canvas by [Ítalo Epifânio](https://github.com/itepifanio).
- Annotator step (explore, create, improve) can be recovered when using Ipyannotator API by [Ítalo Epifânio](https://github.com/itepifanio).
- New documentation theme and structure by [Carlos Cerqueira](https://github.com/Carloscerq) and [Ítalo Epifânio](https://github.com/itepifanio).

## [0.7.0] - 2022-02-19

### Changed
- Updated dependencies to fix Voila's conflict by [Ítalo Epifânio](https://github.com/itepifanio).
- Code is now MyPy compliant by [Carlos Cerqueira](https://github.com/Carloscerq).
- Added `TrajectoryStore` class to improve code readability by [Ítalo Epifânio](https://github.com/itepifanio).

### Fixed
- BBoxAnnotator coordinate's input now changes according to the image size [Ítalo Epifânio](https://github.com/itepifanio).
- Faster right menu rendering, improving overall VideoAnnotator navigation speed by [Ítalo Epifânio](https://github.com/itepifanio).
- Don't draw trajectory for deleted objects in VideoAnnotator by [Ítalo Epifânio](https://github.com/itepifanio).

## [0.6.0] - 2022-01-31

### Added
- New annotator to explore images in a directory (`ExploreAnnotator`) by [Alexander Pisarenko](https://github.com/AlexJoz).
- New annotator for video format (`VideoAnnotator`) by [Ítalo Epifânio](https://github.com/itepifanio).
- New tutorial showing how to use the video annotator by [Ítalo Epifânio](https://github.com/itepifanio).
- New artifical data generator for video by [Carlos Cerqueira](https://github.com/Carloscerq).
- New linter to ensure code standard by [Carlos Cerqueira](https://github.com/Carloscerq).

### Changed
- Updated the CI/CD to add the linter verification by [Carlos Cerqueira](https://github.com/Carloscerq).
- Started to switch classes from Pydantic models to use Attrs by [Ítalo Epifânio](https://github.com/itepifanio).
- Refactored callbacks to use the standard `on_<prefix>_<action>` ex. `on_navi_clicked` by [Ítalo Epifânio](https://github.com/itepifanio).
- Updated dataset download to use `pooch` by [Carlos Cerqueira](https://github.com/Carloscerq).

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
