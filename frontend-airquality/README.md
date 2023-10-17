# Decentralized AQI Classifier

This project demonstrates how to implement a web application UI to interact with [airquality](../airquality/) DApp locally.
It is a specific client for the Airquality application, and is intended to work using any of the `Airquality` projects as the back-end. It is an adapted version of frontend-echo project, using the same structure.

It is implemented as a regular ReactJS application, using [ethers](https://docs.ethers.io/) and [apollo](https://www.apollographql.com/docs/react/) as its main dependencies.

<div align="center">
    
  <a href="">[![Static Badge](https://img.shields.io/badge/cartesi--rollups-1.0.0-5bd1d7)](https://docs.cartesi.io/cartesi-rollups/)</a>
  <a href="">[![Static Badge](https://img.shields.io/badge/react.js-18.0.17-green)](https://react.dev/)</a>
  <a href="">[![Static Badge](https://img.shields.io/badge/ethers-5.7-brown)](https://docs.ethers.io/v5/)</a>
</div>



[AirqualityClassifier.webm](https://github.com/MarcusSouzaLocus/rollups-examples/assets/101931038/441f8945-feab-4c73-a697-94a251f95061)



It interacts with the DApp in two ways:

- Sends inputs to the DApp ([`RoarForm` component](#send-an-input-the-roar-component))
- Queries the DApp for results ([`Echoes` component](#query-outputs-the-echoes-component))

This version is currently restricted to `Airquality` DApps running on localhost using the local Hardhat chain and default test wallet.

## Building

Simply execute the following command from the project's directory:

```shell
yarn
```

## Running

First of all, you should run an `airquality` back-end in your local environment. 

With the DApp running, open a separate terminal in this project's directory, and run:

```shell
yarn start
```

This will execute the front-end application in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## How it works

### Send an Input: the Roar Component

This component presents a Form that captures a string entered by the user, and then sends it as an Input to the Echo DApp.
This component uses [ethers](https://docs.ethers.io/) to interact with the Cartesi Rollups through the blockchain. It follows these simple steps:

- Connects to the blockchain using a provider
- Creates a wallet instance connected to the provider so we can send signed transactions
- Creates a Cartesi `InputFacet` contract instance for the DApp
- Sends an `addInput` transaction using the `InputFacet` contract

## Brief
In general terms, the Decentralized Airquality Classifier offers an interactive, web UI interacting with the backend through a simple inputs based forms.
