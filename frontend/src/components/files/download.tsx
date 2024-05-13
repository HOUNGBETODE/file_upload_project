'use client';

import '../../styles/downloadBtn.css';

export default function DownloadFile({ downloadLink, filename } : { downloadLink: string, filename: string }) {
            
    const handleSubmit = async (event : any) => {
        event.preventDefault();
        // logic code to download the requested file
        fetch(downloadLink)
            .then((res) => res.blob())
            .then(file => {
                let tempURL = URL.createObjectURL(file);
                let aTag = document.createElement('a');
                aTag.href = tempURL;
                aTag.download = filename;
                event.target.appendChild(aTag);
                aTag.click();
                aTag.remove();
                URL.revokeObjectURL(tempURL);
            })
    }

    return (
        <>
            <form onSubmit={handleSubmit}>
                <button type="submit" className="btnd fa fa-download"></button>
            </form>
        </>
    );
}
