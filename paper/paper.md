---
title: 'Ipyannotator: the infinitely hackable annotation framework'
tags:
    - Python
    - Jupyter Notebook
    - Annotator
    - Annotations
authors: 
    - name: Ítalo Epifânio
      affiliation: 1
    - name: Oleksandr Pysarenko
      affiliation: 1
    - name: Immanuel Bayer
      affiliation: 1
affiliations:
    - name: Palaimon GmbH
      index: 1
date: 28 February 2022
bibliography: paper.bib
---

# Summary
Annotation is a task that associates semantic tags to a digital representation (image, video, text, and others). This process is important for supervised machine learning (ML) approaches, since the model learns and successively improves from data examples in form of input-output-pairs.

The variety of digital representations makes it difficult to develop a tool that is flexible and meets all requirements for machine learning applications in different projects. Ipyannotator is an open-source tool that allows manual annotation on multiple data formats, enabling researchers/users to explore, create and improve their datasets without leaving their own development environment, and empowering them to extend and customize the annotation process.

# Statement of need
Many breakthroughs in machine learning (ML) applications such as image classification, text understanding, and recommender systems belong to the class of supervised machine learning. These ML methods often require an extensive basis of annotated data from which the model learns. The amount and quality of the annotated data is essential to generate a model which yields accurate prediction [@wong2015smartannotator].

The variety of annotation taks, data formats, and the respective visualization of data is enormous. Dealing with multiple domains of supervised ML, the large variety of applications is a challenging task considering that the tooling is potentially not flexible enough which imposes limitations to the user.

Ipyannotator is a library developed to provide a solution to this problem. Ipyannotator can be used to visualize, create, and improve datasets, providing a flexible solution that can be extended and customized by the user within the development environment Jupyter.

Jupyter is one of the most popular tools for data science [@wang2019how] and is currently used by more than 7850000 public repositories on GitHub [@parente2022nbestimate]. Ipyannotator is a tool developed to be used on Jupyter Notebook, allowing researchers and developers to integrate the library into their ML projects quickly and easily. The solution, however, is not limited to research and developement teams. Since the Ipyannotator runs also on a web server, it can by used for annotation purposes by any user.

[@lahtinen2021brima] developed an annotator as a browser plugin, [@dutta2019via] built an annotator as a program that runs on the browser, and [@bernal2019gtcreator] developed a desktop application for domain-specific medical image annotation. The previous annotation tools are restricted to fixed data types and a specific type of annotation. Ipyannotator was designed to be executed in Jupyter notebooks and allows users to change its iterations on runtime, allowing extensions and customization, creating an "infinitely hackable annotation framework" [^1].

[^1]: "infinitely hackable" is one of the key design principles used. Even through using very thin python wrappers e.g. [@ipycanvas2022] for the JavaScript Web Canvas API, ipyannotator still has to obey the finite limitations of the python language.

# Infinitely hackable annotation framework
Ipyannotator uses Python libs, such as Ipywidgets [@ipywidgets2022], Ipycanvas [@ipycanvas2022] and Ipyevents [@ipyevents2022], that abstract the HTML and Javascript interactions, allowing developers to design UI interactions and elements using Python. Python's dynamic nature allows users to modify classes or modules in runtime, due to the libs mentioned, users can change the default behavior of Ipyannotator's UI, hacking the library. Browser interaction like mouse moving and HTML elements like dropdowns are some of the examples that can be changed at runtime when using Ipyannotator.

Being integrated with Jupyter notebooks makes Ipyannotator usage easy to modify at different abstraction levels. The data science team can change the library behavior while writing their own scripts on a platform and programming language that they already know.

In addition to the ability to change Ipyannotator's browser interaction using Python, the library also provides a flexible API that enables adding custom annotators. With a custom pair of input and output classes, the user can create and register a new annotator while reusing the library resources.

# A simple but flexible API to define annotation tasks
Ipyannotator provides a simple API (application programming interface) which is based on three steps describing general tasks in the data annotation process. These are denoted as the explore, create, and improve phase.

These three steps in conjuction with domain-specific annotation types, define the inputs and outputs of the annotation process, providing a very flexible and extendable API to set up annotation tasks.

The following code examples illustrate the main actions around which the Ipyannotator API is built. Please keep in mind that Ipyannotator aims to be flexible enought so that these generic aspects can be extented to much complexer and domain-specific tasks and interfaces. As an exemplary application, a standard image classification task, is used in the following.

```python
from pathlib import Path
from ipyannotator.base import Settings
from ipyannotator.annotator import Annotator
from ipyannotator.mltypes import InputImage, OutputImageLabel

input = InputImage(image_dir='images', image_width=200, image_height=200)
output = OutputImageLabel(label_dir='labels', label_width=30, label_height=30)
settings = Settings(project_path=Path('data'))

annotator = Annotator(input, output, settings)
```

## Explore
The explore step provides the ability to visualize and navigate through images and datasets. \autoref{fig:image-classification-explore} displays an example of an image classification task using one of Ipyannotator's inbuilt artificial demonstration datasets.
The dataset consists of images showing simple shapes in different colors. The annotation task is to assign to each image the color which is closest to the provided labels.

![Explore step for image classification task\label{fig:image-classification-explore}](image-classification-explore.png){ width=60% }

## Create
In the create step new annotation datasets can be created by the user. \autoref{fig:image-classification-create} presents an example of an image classfication task, allowing the user to manually select multiple options and save the results in the dataset.

![Create step for image classification task \label{fig:image-classification-create}](image-classification-create.png)

## Improve
The improve step enables the user to refine datasets and, thereby, improve the annotation quality. \autoref{fig:image-classification-improve} displays the improve usage, allowing users to iterate over every class and identify incorrect results.

Inspecting large batches of pre-annotated data allows to very quickly improve the quality of datasets that were generated by an insufficient ML model. It also allows a domain expert to verify and improve the annotation work of less specialized annotators.

![Improve step for image classification task \label{fig:image-classification-improve}](image-classification-improve.png){ width=60% }

# Key Design Decisions
## Jupyter Notebook all the way down
Jupyter Notebook is used by many researcher relaying on open source software to create and document their work.
Ipyannotator not only runs directly in Jupyter Notebook but is also developed as a collection of notebooks. This collection
constitues a library, user documentation, and executable tutorials. This workflow is enabled by the innovative fastai library [@nbdev2022] that turns Jupyter Notebook into a literate programming environment.

For the development of the user interface (UI) the Ipywidget library [@ipywidgets2022] was used to build a graphical user interface (GUI) in Jupyter Notebook. Furthermore, the voila library [@voila2022], which uses Jupyter Notebook as a web-app, was also incorporated in the Ipayannotator project to create the GUI for an easy to access web application.

## Architecture
Ipyannotator's architecture consists of three main systems components that comprise the user interface (UI), the server, and the data storage. These components are targeted at two different user types. A non-code architecture, which is schematically illustrated in \autoref{fig:non-technical-annotator}, is included for non-technical annotators. The setup for a wide range of technically experienced annotators, schematically shown in \autoref{fig:technical-user-architecture}, target users typically involved in research projects, e.g. data scientists, domain experts, and software developer.

![Non-technical user architecture  \label{fig:non-technical-annotator}](non-technical-user-architecture.png){ width=60% }

![Technical user architecture  \label{fig:technical-user-architecture}](technical-user-architecture.png){ width=52% }

For the technical user multiple tutorials are provided, demonstrating Ipyannotator's utilization. The tutorials make it easier for new users get started and adapt the notebooks to their tasks. They also demonstrate annotation workflow and different features.

# Usage

Currently, Ipyannotator is used for supervised ML projects by the devloper Palaimon GmbH. Multiple tutorials and use cases have been tested and published to improve and validate the usage of Ipyannotator on other real world projects.

# Acknowledgements

The authors acknowledge the financial support by the Federal Ministry for Digital and Transport of Germany under the program mFUND for the project OS-VAT (project number 19F2160A).

# References
