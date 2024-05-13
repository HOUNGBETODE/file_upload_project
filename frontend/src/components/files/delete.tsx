import '../../styles/deleteBtn.css';

import { deleteFile } from '@/actions/files';

export default function DeleteFile({ token, fileId, funct2 } : { token: string, fileId: string, funct2: Function }) {
    
    const deleteFileWithToken = deleteFile.bind(null, token);
    const deleteFileWithTokenAndId = deleteFileWithToken.bind(null, fileId);

    return (
        <>
            <form action={deleteFileWithTokenAndId} onSubmit={(event) => {
                                                                        funct2('miba');
                                                                        console.log(event)
                                                                        {setTimeout(() => {
                                                                            funct2('')
                                                                        }, 10)}
                                                                    }}
            >
                <button className="btnx danger fa fa-trash" type="submit"></button>
            </form>
        </>
    );
}
