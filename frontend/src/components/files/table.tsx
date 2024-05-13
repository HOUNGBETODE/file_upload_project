'use client';

import { formatDateToLocal } from "@/utils/utils";
import { FileSchema } from "@/app/lib/definitions";
import DeleteFile from "./delete";
import DownloadFile from "./download";


export default function FilesTable({ filesList, token, funct1 } : { filesList: FileSchema[], token: string, funct1: Function }) {
    
    return (
        <>
            <table className="center">
                <thead>
                    <tr>
                        <th>N°</th>
                        <th>Filename</th>
                        <th>Horodatage</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {filesList.map((file, index) => {
                        if(file?.upload_dateinfos && file?.document && file?.link && file?.id) {
                            return (<tr key={index}>
                                <td>{++index}</td>
                                <td>{file?.document}</td>
                                <td>{formatDateToLocal(file?.upload_dateinfos)}</td>
                                <td>
                                    <div className="btns">
                                        <DownloadFile downloadLink={file?.link} filename={file?.document} />
                                        <br />
                                        <DeleteFile token={token} fileId={file?.id} funct2={funct1} />
                                    </div>
                                </td>
                            </tr>)
                        }
                    })}
                </tbody>
            </table>
        </>
    );
}
