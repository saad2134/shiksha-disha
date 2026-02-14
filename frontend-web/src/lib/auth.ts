export interface LoginData {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface SignupData {
  name: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  user?: {
    id: string;
    name: string;
    email: string;
  };
  token?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

export const authService = {
  async login(data: LoginData): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Non-JSON response:', text);
        return {
          success: false,
          message: 'Server error. Please try again later.',
        };
      }

      const result = await response.json();
      
      if (response.ok && result.success) {
        if (result.token) {
          localStorage.setItem('auth_token', result.token);
        }
        if (data.rememberMe) {
          localStorage.setItem('remember_email', data.email);
        }
      }
      
      return result;
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        message: 'Unable to connect to server. Please try again.',
      };
    }
  },

  async signup(data: SignupData): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Non-JSON response:', text);
        return {
          success: false,
          message: 'Server error. Please try again later.',
        };
      }

      const result = await response.json();
      
      if (response.ok && result.success) {
        if (result.token) {
          localStorage.setItem('auth_token', result.token);
        }
      }
      
      return result;
    } catch (error) {
      console.error('Signup error:', error);
      return {
        success: false,
        message: 'Unable to connect to server. Please try again.',
      };
    }
  },

  async googleAuth(): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/google`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Non-JSON response:', text);
        return {
          success: false,
          message: 'Server error. Please try again later.',
        };
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Google auth error:', error);
      return {
        success: false,
        message: 'Unable to connect to server. Please try again.',
      };
    }
  },

  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('remember_email');
  },

  getStoredEmail(): string {
    return localStorage.getItem('remember_email') || '';
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  },
};
