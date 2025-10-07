import Footer from "@/components/sections/footer/default";
import Navbar from "@/components/sections/navbar/default";
import Glow from "@/components/ui/glow";

export const metadata = {
  title: "Privacy Policy | ShikshaDisha",
  description: "Learn how ShikshaDisha collects, uses, and protects your personal information.",
};

export default async function Privacy() {
  return (
    <>

      <main className="min-h-screen w-full overflow-hidden bg-background text-foreground">
        <Navbar />

        <section className="mx-auto max-w-4xl px-12 py-12 pt-32 md:pt-32 sm:gap-48">
          <h1 className="text-3xl font-bold mb-6">Privacy Policy</h1>
          <p className="text-sm text-muted-foreground mb-10">Last Updated: October 2025</p>

          <div className="prose prose-neutral dark:prose-invert max-w-none space-y-6">
            <p>
              At <strong>ShikshaDiksha</strong>, we respect your privacy and are committed to protecting your
              personal information. This Privacy Policy explains how we collect, use, and safeguard your data
              when you use our Service.
            </p>

            <h2>1. Information We Collect</h2>
            <ul>
              <li>Basic profile details (education, skills, learning goals).</li>
              <li>Usage data (how you interact with the Service).</li>
              <li>Optional information you provide during onboarding or feedback.</li>
            </ul>

            <h2>2. How We Use Your Information</h2>
            <p>Your data is used to:</p>
            <ul>
              <li>Provide personalized learning recommendations.</li>
              <li>Improve the accuracy and relevance of the Service.</li>
              <li>Communicate updates, changes, and relevant opportunities.</li>
            </ul>

            <h2>3. Data Sharing</h2>
            <p>
              We do not sell, rent, or trade your personal information. Data may only be shared:
            </p>
            <ul>
              <li>With trusted service providers who help operate the Service.</li>
              <li>When required by law or government authorities.</li>
            </ul>

            <h2>4. Data Security</h2>
            <p>
              We take appropriate measures to protect your personal data against unauthorized access,
              alteration, or disclosure. However, no method of transmission over the Internet is 100% secure.
            </p>

            <h2>5. Your Rights</h2>
            <ul>
              <li>You may request access, correction, or deletion of your personal data.</li>
              <li>You can opt out of communications at any time.</li>
            </ul>

            <h2>6. Children’s Privacy</h2>
            <p>
              The Service is not intended for children under the age of 13. We do not knowingly collect personal
              data from children.
            </p>

            <h2>7. Changes to This Policy</h2>
            <p>
              We may update this Privacy Policy occasionally. Updates will be effective immediately upon
              posting. Continued use of the Service means you accept the revised policy.
            </p>

            <h2>8. Contact Us</h2>
            <p>
              If you have questions about this Privacy Policy, contact us at:{" "}
              <a href="mailto:reach.saad@outlook.com" className="text-primary underline">
                reach.saad@outlook.com
              </a>
            </p>
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
