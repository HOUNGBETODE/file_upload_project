import { z } from 'zod'

export const LoginFormSchema = z.object({
  username: z
    .string()
    .trim()
    .refine((value) => value !== "", {
      message: "Username must not be empty.",
    }),
  password: z
    .string()
    // // .min(8, { message: 'Be at least 8 characters long' })
    // .regex(/[a-zA-Z]/, { message: 'contain at least one letter.' })
    // .regex(/[0-9]/, { message: 'contain at least one number.' })
    // .regex(/[^a-zA-Z0-9]/, {
    //   message: 'contain at least one special character.',
    // })
    .trim()
    .refine((value) => value.trim() !== "", {
      message: "Password must not be empty.",
    })
});

export const RegisterFormSchema = z.object({
  username: z
    .string()
    .min(3, { message: 'be at least 3 characters long' })
    .trim()
    .refine((value) => value.trim() !== "", {
      message: "not be empty.",
    })
    .refine((value) => !value.trim().includes(" "), {
      message: "contain no space.",
    }),
  email: z
    .string()
    .email({ message: 'This is not a valid email address.' }),
  password1: z
    .string()
    .min(8, { message: 'be at least 8 characters long' })
    .regex(/[a-zA-Z]/, { message: 'contain at least one letter.' })
    .regex(/[0-9]/, { message: 'contain at least one number.' })
    .regex(/[^a-zA-Z0-9]/, {
      message: 'contain at least one special character.',
    })
    .trim()
    .refine((value) => value.trim() !== "", {
      message: "not be empty.",
    }),
  password2: z
    .string()
    .refine((value) => value.trim() !== "", {
      message: "This field could not be empty.",
    }),
  genre: z
    .enum(['male', 'female'], { message: "You need to select a genre value." })
})
 
export type FormState =
  | {
      errors?: {
        username?: string[]
        email?: string[]
        genre?: string[]
        password?: string[]
        password1?: string[]
        password2?: string[]
      }
      message?: string,
    }
  | undefined

export type SessionPayload = 
  | {
      accessToken?: string,
      refreshToken?: string,
      username?: string,
      expiresAt?: object,
      iat?: number,
      exp?: number
    }
  | undefined

export type FileSchema = 
  | { 
      id: string, 
      document: string, 
      upload_dateinfos: string,
      link: string 
    }
  | undefined