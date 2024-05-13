import { cookies } from 'next/headers';
import { decrypt } from '../lib/session';
import { SessionPayload } from '../lib/definitions';
import LogOut from '@/components/auth/logout';
import Main from '@/components/greetNload';

export default async function Home() {
    const sessionStore : SessionPayload | undefined = await decrypt(cookies().get('session')?.value);
    const token : string | undefined = sessionStore?.accessToken;
    const username : string | undefined = sessionStore?.username;

    if(token && username) {
        return (
            <body className='u-body'>
                    <div className="u-container">
                        <LogOut />
                        <Main username={username} token={token} />
                    </div>
            </body>
        );
    }
}
