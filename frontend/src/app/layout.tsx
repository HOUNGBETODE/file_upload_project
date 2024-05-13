export const metadata = {
  title: 'NextFileUploadApp',
  description: 'Done by HOUNGBETODE Ange using Next.js',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      {/* <body> */}
      {/* <div className="topnav">
        <Link className="active" href="/login">Login</Link>
        <Link href="/home">Home</Link>
        <Link href="/profile">Profile</Link>
        <Link href="/logout">Logout</Link>
      </div> */}
          {children}
      {/* </body> */}
    </html>
  )
}
