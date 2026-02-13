import { NextResponse } from 'next/server';

interface Service {
  name: string;
  url: string;
}

const services: Service[] = [
  { name: "Frontend Web (Vercel)", url: "https://vercel.app" },
];

async function checkService(url: string): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    const res = await fetch(url, { method: "HEAD", signal: controller.signal });
    clearTimeout(timeoutId);
    return res.ok;
  } catch {
    return false;
  }
}

export async function GET() {
  const results = await Promise.all(
    services.map(async (service) => {
      const status = await checkService(service.url);
      return {
        name: service.name,
        url: service.url,
        status,
        timestamp: new Date().toISOString(),
      };
    })
  );

  const allOperational = results.every((result) => result.status);
  const hasIssues = results.some((result) => !result.status);

  return NextResponse.json({
    status: allOperational ? 'operational' : hasIssues ? 'issues' : 'degraded',
    services: results,
    checkedAt: new Date().toISOString(),
  });
}
