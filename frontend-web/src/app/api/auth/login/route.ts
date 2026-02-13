import { NextResponse } from 'next/server';

const DB_URL = process.env.DATABASE_URL || process.env.NEXT_PUBLIC_API_URL || '';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { email, password, rememberMe } = body;

    if (!email || !password) {
      return NextResponse.json(
        { success: false, message: 'Email and password are required' },
        { status: 400 }
      );
    }

    if (!DB_URL) {
      return NextResponse.json(
        { success: false, message: 'Database configuration missing' },
        { status: 503 }
      );
    }

    try {
      const dbResponse = await fetch(`${DB_URL}/api/users/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
        signal: AbortSignal.timeout(10000),
      });

      if (!dbResponse.ok) {
        const errorData = await dbResponse.json().catch(() => ({}));
        return NextResponse.json(
          { success: false, message: errorData.message || 'Invalid credentials' },
          { status: 401 }
        );
      }

      const userData = await dbResponse.json();

      if (!userData.success) {
        return NextResponse.json(
          { success: false, message: userData.message || 'Invalid credentials' },
          { status: 401 }
        );
      }

      return NextResponse.json({
        success: true,
        message: 'Login successful',
        user: userData.user || {
          id: '1',
          name: email.split('@')[0],
          email,
        },
        token: userData.token || 'demo-token-' + Date.now(),
      });
    } catch (dbError) {
      console.error('Database connection failed:', dbError);
      return NextResponse.json(
        { success: false, message: 'Unable to connect to database. Please try again later.' },
        { status: 503 }
      );
    }
  } catch {
    return NextResponse.json(
      { success: false, message: 'Invalid request' },
      { status: 400 }
    );
  }
}
