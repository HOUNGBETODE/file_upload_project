import 'server-only';

import { SignJWT, jwtVerify } from 'jose';
import { SessionPayload } from './definitions';
import { cookies } from 'next/headers';

const secretKey = process.env.SESSION_SECRET
const encodedKey = new TextEncoder().encode(secretKey)


export async function createSession(accessToken: string, refreshToken: string, username: string) {
    const expiresAt = new Date(Date.now() + 30 * 60 * 1000)
    const session = await encrypt({ accessToken, refreshToken, username, expiresAt })
   
    cookies().set('session', session, {
      httpOnly: true,
      secure: true,
      expires: expiresAt,
      sameSite: 'lax',
      path: '/',
    })
}


export async function encrypt(payload: SessionPayload) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('30min')
    .sign(encodedKey)
}


export async function decrypt(session: string | undefined = '') {
  try {
    const { payload } = await jwtVerify(session, encodedKey, {
      algorithms: ['HS256'],
    })
    return payload
  } catch (error) {
    console.log('Failed to verify session')
  }
}


export function deleteSession() {
    cookies().delete('session');
}