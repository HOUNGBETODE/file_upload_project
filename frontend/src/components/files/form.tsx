import { uploadFile } from "@/actions/files";

export default function FilesForm({ token } : {
    token: string | undefined
}) {
    const uploadFileWithToken = uploadFile.bind(null, token);

    return (
        <>
            <body className="u-body">
                <div className="u-container">
                    <form className="u-form" action={uploadFileWithToken}>
                        <input type="file" name="file" id="file" required />
                        <br />
                        <button className="upl" type="submit">Submit</button>
                    </form>
                </div>
            </body>
        </>
    );
}
