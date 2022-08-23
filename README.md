# PyPos Canteen - Point of Sale Web Application

Point of sale web app aimed to work on a low-budget canteen setup.

[Video Presentation](https://youtu.be/jJ_M1ueIH9g) | [Live Demo](http://pypos-env.eba-vnvdpu3c.us-west-2.elasticbeanstalk.com/)

## Overview

Pypos is a Point of Sale web application aimed to be easily implemented in a small scholar canteen with ease. The key features are cashless payment (a user credit system), basics and insightful financial reporting, and offline support (not implemented in this version yet).

I began thinking about this project when my girlfriend was working in a scholar canteen that didn't have any point of sale software and which accepted credit payment. It was a mess and she was getting upset. We didn't find a good and affordable service that suited the canteen needs, so back then I made a quick solution with Airtable.

Now she doesn't work there anymore, but as I was quite familiar with the business requisites, I've decided to go on and submit it as the final project on the CS50 course. I didn't manage to make the UX and features as good as I wanted, but it worked as a proof of concept.

---

The system aims to:

* Let the sales quickly record transactions in the POS interface with little effort.
* Manage credit sales with ease and little bureaucracy in a relatively low user base (200-1000 users per canteen).
* Display simple and solid financial and client habits reports and insights.
* Let children buy food without the need to handle money directly.

The system doesn't aim to:

* Be extremely scalable
* Be a complete ERP or financial management tool.
* Integrate with credit and debit card services.

## Run Locally

TODO

## Design and Technical Choices

The project was built mostly with the tools taught in the course. On the backend, I've used Flask and Sqlite, and at some point, [Pydantic](https://pydantic-docs.helpmanual.io/) was introduced as well (it helped to make the validation system more elegant). On the front end, I've used the Bootstrap 5 framework and some custom Javascript. JS was mainly used in the point of sale page, which is the most complex user interface of the application.

If you want to read more about technical and design consideration, [checkout my blog](https://pedro-psb.github.io/)!
