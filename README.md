# Overview

This project is intended to be an easy deployable and cheap solution for a canteen system. It is a beta project, so it may take some time to get ready to production.

# Features

## Account/credit system

Users can have virtual account, so they can put money into it and buy from the cantinee cacheless. This have two advantages: the kids don't have to deal with money (altough they could, to put more money for example) and the buying process is faster, making the lines more agile.

## Integrated stock control/ sales report

The point of sale will register the amount of products being sold. It can provide reports on the cash register transactions and on stock.

## Offline support

The system will be designed to work with intermitent internet connection: before a session you must fetch the updated database from the server, and after the session you should pull the changes. The system is not designed to deal with multiple database acesses just yet.

## PagSeguro integration

The system should support integration with PagSeguro, a brazillian company for online sales. The main purpose the integration is to automatic update the system credits when users transfer money to the Pag Seguro account.

# Implementation

The project is build with Flask, a python micro-framework made for wep app development.

# Deploy and Usage

You can deploy where you prefer, but it is aimed to work on Heroku, which is easy to setup and has a free tier.

TODO tutorial on deploying and using
