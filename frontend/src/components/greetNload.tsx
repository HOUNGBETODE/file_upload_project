'use client';

import { aUserUploadedFiles } from "@/actions/files";
import FilesList from "./files/list";
import { useState, useEffect } from "react";
import Link from "next/link";

export default function Main({ username, token } : { username: string, token: string }) {
    const [pattern, setPattern] = useState('');
    const [files, setFiles] = useState([]);
    const [isLoading, setLoading] = useState(true);

    const handleChange = async (event : any) => {
        setPattern(event.target.value);
    }


    useEffect(() => {
        const update = async () => {
            // setLoading(true);
            setFiles([await aUserUploadedFiles(token, pattern)][0]);
            setLoading(false);
        };
        update();
        console.log({pattern})
    }, [token, pattern]);

    return (
        <>
            <h2>Welcome { username }</h2>
                <hr />
                <div className="h-container">
                    <div className="input-container">
                        <input type="text" placeholder="Search.." onChange={handleChange} />
                    </div>
                    <div className="link-btn">
                        <Link href="/home/form"><button >Upload file</button></Link>
                    </div>
                </div>
                <hr />
                <FilesList token={token} pattern={pattern} files={files} loading={isLoading} funct={setPattern}/>
        </>
    );
}
