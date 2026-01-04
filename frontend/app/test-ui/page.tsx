// Simple test page without any auth or complex logic
export default function TestUIPage() {
  console.log("✅ Test UI Page Loaded Successfully!");

  return (
    <div style={{
      padding: '50px',
      backgroundColor: '#013630', /* emerald-950 */
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '20px'
    }}>
      <h1 style={{
        fontSize: '48px',
        color: '#fff', /* white */
        fontWeight: 'bold',
        margin: 0
      }}>
        UI is Working! ✅
      </h1>
      <p style={{
        fontSize: '20px',
        color: '#c7f3e6', /* emerald-200/300 equivalent */
        textAlign: 'center',
        maxWidth: '600px'
      }}>
        If you can see this message, Next.js is rendering correctly.
        There are no auth checks or redirects on this page.
      </p>
      <div style={{
        padding: '20px',
        backgroundColor: '#10b981', /* emerald-500 */
        color: 'white',
        borderRadius: '16px', /* rounded-2xl equivalent */
        fontSize: '18px'
      }}>
        Frontend is functional!
      </div>
    </div>
  );
}
