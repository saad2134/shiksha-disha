import { NextResponse } from 'next/server';

const DB_URL = process.env.DATABASE_URL || process.env.NEXT_PUBLIC_API_URL || '';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, email, password } = body;

    if (!name || !email || !password) {
      return NextResponse.json(
        { success: false, message: 'Name, email and password are required' },
        { status: 400 }
      );
    }

    if (password.length < 6) {
      return NextResponse.json(
        { success: false, message: 'Password must be at least 6 characters' },
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
      const dbResponse = await fetch(`${DB_URL}/api/users/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
        signal: AbortSignal.timeout(10000),
      });

      if (!dbResponse.ok) {
        const errorData = await dbResponse.json().catch(() => ({}));
        return NextResponse.json(
          { success: false, message: errorData.message || 'Registration failed' },
          { status: dbResponse.status }
        );
      }

      const userData = await dbResponse.json();

      if (!userData.success) {
        return NextResponse.json(
          { success: false, message: userData.message || 'Registration failed' },
          { status: 400 }
        );
      }

      return NextResponse.json({
        success: true,
        message: 'Account created successfully',
        user: userData.user || {
          id: '1',
          name,
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
