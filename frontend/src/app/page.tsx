'use client';

import Link from "next/link";
import styled from "styled-components";

const IndexBody = styled.body`
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
`

export default function Index() {
    return (
        <IndexBody>
            <p>To start interacting with our app, please, go to <Link href="/signin">login</Link> page.</p>
        </IndexBody>
    );
}