'use client';

import '../../styles/register.css';

import { registerUser } from '@/actions/auth';
import { useFormState } from 'react-dom';

export default function Register() {
    const [state, registerAction] = useFormState(registerUser, undefined);

    return (
        <>
            <body className='r-body'>
                <form className='r-form' action={registerAction} >
                    <div className="container">
                    <h1>Sign Up</h1>
                    <p className='desc'>Please fill in this form to create an account.</p>
                    <hr />

                    <label htmlFor="username"><b>Username</b></label>
                    <input type="text" placeholder="Enter Username" name="username" 
                        onKeyDown={(event) => {
                            if (event.keyCode === 32) {
                            event.preventDefault();
                            }
                        }} 
                    />
                    {state?.errors?.username && (
                        <div className="error">
                            <p>Username must:</p>
                            <ul>
                            {state.errors.username.map((error) => (
                                <li key={error}>- {error}</li>
                            ))}
                            </ul>
                        </div>
                    )}
                
                    <label htmlFor="email"><b>Email</b></label>
                    <input type="text" placeholder="Enter Email" name="email"  />
                    {state?.errors?.email && <div className="error"><p>{state.errors.email}</p></div>}
                
                    <label htmlFor="psw"><b>Password</b></label>
                    <input type="password" placeholder="Enter Password" name="password"  />
                    {state?.errors?.password1 && (
                        <div className="error">
                            <p>Password must:</p>
                            <ul>
                            {state.errors.password1.map((error) => (
                                <li key={error}>- {error}</li>
                            ))}
                            </ul>
                        </div>
                    )}
                
                    <label htmlFor="psw-repeat"><b>Repeat Password</b></label>
                    <input type="password" placeholder="Repeat Password" name="passwordrepeat"  />  
                    {state?.errors?.password2 && <div className="error"><p>{state.errors.password2}</p></div>}

                    <label htmlFor="genre"><b>Genre</b></label> <br />
                    <label className="r-container">Male
                        <input type="radio" name="genre" value="male"  />
                        <span className="checkmark"></span>
                    </label>
                    <label className="r-container">Female
                        <input type="radio" name="genre" value="female"  />
                        <span className="checkmark"></span>
                    </label>
                    {state?.errors?.genre && <div className="error"><p>{state.errors.genre}</p></div>}
                
                    <div className="clearfix">
                        {state?.message && <p className="error" >{state.message}</p>}
                        <button type="submit" className="signupbtn">Register</button>
                    </div>
                    </div>
                </form>
            </body>
        </>
    )
}