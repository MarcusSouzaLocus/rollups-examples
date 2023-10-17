import "./App.css";
import RoarForm from "./RoarForm";
import Echoes from "./Echoes";
import React, { useState } from "react";
import { Flex, Box, Heading, Container } from "@chakra-ui/react";

function App() {
    const [accountIndex] = useState(0);

    return (
        <div className="App">
            <AppHeader />
            <Container maxW="container.lg" mt={6}>
                <Flex justify="space-between">
                    <RoarForm accountIndex={accountIndex} />
                    <Echoes />
                </Flex>
            </Container>

            <AppFooter />
        </div>
    );
}

function AppHeader() {
    return (
        <Box as="header" bg="linear-gradient(90deg, #182848, #182848)" p={6} shadow="md">
            <Heading as="h1" size="2xl" color="white" textAlign="center">
                Decentralized AQI Classifier
            </Heading>
        </Box>
    );
}

function AppFooter() {
    return (
        <Box as="footer" bg="gray.800" p={4} mt={6}>
            <Heading as="h6" size="sm" color="gray.300" textAlign="center">
                Marcus Souza - 2023 - https://www.linkedin.com/in/marcus-vini-souza/
            </Heading>
        </Box>
    );
}

export default App;
