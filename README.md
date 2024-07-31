# ReelBlend - Vision Engine

This repository contains Python webserver containing a AI enabled computer-vision engine to analyze videos/scenes and generate response against it.

Our Vision Engine module resting inside the back-end engine ingests a video via Back-end REST API, analyses it using Computer Vision and AI Algorithms and outputs a response based on what is being queried for. 

The response contains any or all of the following:
* Scene Analysis
* Object Detection
* Object Tracking
* Segmentation Masks
* More TBD

[Related Engineering Docs](https://reelblend.slab.com/posts/tech-stack-wv9y1177)

## Overview
- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
- [Usage](#usage)
- [Outputs](#outputs)
- [Environment variables](#environment-variables)
- [Backend](#Backend)
- [Computer Vision models used](#computer-vision-models-used)
- [Video considerations](#video-considerations)

### Pre-requisites

*TBD*


### Installation

1. Clone the repository to your local machine.

  > https://github.com/Perioko/Python-Vision-Engine.git

*Next Steps: TBD*


### Usage

*TBD*



### Outputs/Responses:

*TBD*


### Environment variables

*TBD*


### Backend

- Framework: FastAPI
- Database: *TBD*
- API Documentation: Swagger
- API Type: RESTful


### Computer vision models used
All detection us currently performed for object tracking. However we plan to improve for Segmentation in the future (goal to detect walls and other surfaces)

- *TBD*


Training Data:

*TBD*


### Video considerations

- Ensure files are in .mp4 format
- Ensure video duration is not more than 30 seconds.
- Note: Video resolutions lower than 720p may not give optimal detection results.
