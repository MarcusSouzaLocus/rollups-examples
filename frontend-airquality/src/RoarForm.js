import React, { useState } from "react";
import { JsonRpcProvider } from "@ethersproject/providers";
import { ethers } from "ethers";
import { InputBox__factory } from "@cartesi/rollups";
import {Input, Button, useToast, Flex} from "@chakra-ui/react";

const DAPP_ADDRESS = "0x70ac08179605AF2D9e75782b8DEcDD3c22aA4D0C";
const INPUTBOX_ADDRESS = "0x59b22D57D4f067708AB0c00552767405926dc768";
const HARDHAT_DEFAULT_MNEMONIC =
    "test test test test test test test test test test test junk";
const HARDHAT_LOCALHOST_RPC_URL = "http://localhost:8545";

function RoarForm() {
    const [co, setCO] = useState("");
    const [nmhc, setNMHC] = useState("");
    const [nox, setNOx] = useState("");
    const [no2, setNO2] = useState("");
    const [o3, setO3] = useState("");
    const [temperature, setTemperature] = useState("");
    const [humidity, setHumidity] = useState("");
    const [absoluteHumidity, setAbsoluteHumidity] = useState("");
    const [accountIndex] = useState(0);
    const toast = useToast();
    const [loading, setLoading] = useState(false);

    function handleSubmit(event) {
        event.preventDefault();
        const concatenatedString = `${co},${nmhc},${nox},${no2},${o3},${temperature},${humidity},${absoluteHumidity}`;
        const sendInput = async () => {
            setLoading(true);
            const provider = new JsonRpcProvider(HARDHAT_LOCALHOST_RPC_URL);
            const signer = ethers.Wallet.fromMnemonic(
                HARDHAT_DEFAULT_MNEMONIC,
                `m/44'/60'/0'/0/${accountIndex}`
            ).connect(provider);

            const inputBox = InputBox__factory.connect(
                INPUTBOX_ADDRESS,
                signer
            );

            const inputBytes = ethers.utils.isBytesLike(concatenatedString)
                ? concatenatedString
                : ethers.utils.toUtf8Bytes(concatenatedString);

            const tx = await inputBox.addInput(DAPP_ADDRESS, inputBytes);
            toast({
                title: "Transaction Sent",
                description: "waiting for confirmation",
                status: "success",
                duration: 9000,
                isClosable: true,
                position: "top-left",
            });

            const receipt = await tx.wait(1);
            const event = receipt.events?.find((e) => e.event === "InputAdded");

            setLoading(false);
            toast({
                title: "Transaction Confirmed",
                description: `Input added => index: ${event?.args.inputIndex} `,
                status: "success",
                duration: 9000,
                isClosable: true,
                position: "top-left",
            });
        };
        sendInput();
    }

    return (
        <div style={{
            padding: "2rem",
            maxWidth: "600px",
            margin: "auto",
            background: "linear-gradient(90deg, #4b6cb7, #182848)",  // Background em gradiente
            borderRadius: "10px"
        }}>
            <h2 style={{
                textAlign: "center",
                marginBottom: "1.5rem",
                fontWeight: "bold",
                fontSize: "1.5rem",
                color: "white"
            }}>
                Decentralized AQI Classifier
            </h2>
            <form onSubmit={handleSubmit}>
                <Flex direction="row" wrap="wrap" justify="space-between">
                    {[
                        { label: "Carbon Monoxide (CO):", value: co, setter: setCO, placeholder: "0-3000" },
                        { label: "NM Hydrocarbons (NMHC):", value: nmhc, setter: setNMHC, placeholder: "0-3000"},
                        { label: "Nitrogen Oxides (NOx):", value: nox, setter: setNOx,placeholder: "0-3000" },
                        { label: "Nitrogen Dioxide (NO2):", value: no2, setter: setNO2, placeholder: "0-3000" },
                        { label: "Ozone (O3):", value: o3, setter: setO3, placeholder: "0-3000"},
                        { label: "Temperature (T):", value: temperature, setter: setTemperature, placeholder: "In Degrees (Cº)" },
                        { label: "Relative Humidity (RH):", value: humidity, setter: setHumidity, placeholder: "0.0 - 100.0" },
                        { label: "Absolute Humidity (AH):", value: absoluteHumidity, setter: setAbsoluteHumidity, placeholder: "0.0 - 10.0" },
                    ].map((item, index) => (
                        <div key={index} style={{ marginBottom: "1.5rem", flex: "0 0 calc(50% - 1rem)" }}>
                            <p style={{
                                marginBottom: "0.5rem",
                                fontSize: "1.1rem",
                                color: "white"  // Rótulos em branco
                            }}>
                                {item.label}
                            </p>
                            <Input
                                type="number"
                                focusBorderColor="yellow"
                                size="md"
                                value={item.value}
                                placeholder={item.placeholder}
                                style={{ borderRadius: "5px", backgroundColor: "rgba(255,255,255,0.2)" }}
                                onChange={(e) => item.setter(e.target.value)}
                            />
                        </div>
                    ))}
                </Flex>
                <div style={{ textAlign: "center", marginTop: "1rem" }}>
                    <Button type="submit" colorScheme="yellow" isLoading={loading} style={{ borderRadius: "5px" }}>
                        Check AQI
                    </Button>
                </div>
            </form>
        </div>
    );


}

export default RoarForm;
