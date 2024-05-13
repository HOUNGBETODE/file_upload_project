'use client';

import '../../styles/upload.css';
import '../../styles/fileTable.css'

import { FileSchema } from '@/app/lib/definitions';
import FilesTable from "./table";
import { Loader } from '@/styles/loader';

export default function FilesList({ token, pattern, files, loading, funct } :
                             { token: string, pattern: string, files: FileSchema[], loading: boolean, funct: Function }) 
{
    if(files?.length) {
        return (
            <>
                <FilesTable filesList={files} token={token} funct1={funct} />
            </>
        );
    } else {
        if(loading) {
            return (
                <>
                    <center>
                        <Loader />
                    </center>
                </>
            );
        } else {
            return (
                <>
                    <p>{pattern ? 'No matches found' : 'No files uploaded yet'}</p>
                </>
            );
        }
    }
}
