import FilesForm from "@/components/files/form";
import { cookies } from "next/headers";
import { decrypt } from "@/app/lib/session";
import { SessionPayload } from "@/app/lib/definitions";

export default async function Form() {
    const sessionStore : SessionPayload | undefined = await decrypt(cookies().get('session')?.value);
    const token : string | undefined = sessionStore?.accessToken;

    return (
        <div className="container">
            <FilesForm token={token} />
        </div>
    );
}