import Footer from "@/components/sections/footer/default";
import Navbar from "@/components/sections/navbar/default";
import Glow from "@/components/ui/glow";

export const metadata = {
  title: "Contact Us | ShikshaDisha",
  description: "Get in touch with the ShikshaDisha team for support, inquiries, or feedback.",
};


export default async function Contact() {
  return (
    <>

      <main className="min-h-screen w-full overflow-hidden bg-background text-foreground">
        <Navbar />

        <section className="mx-auto max-w-4xl px-12 py-12 pt-32 md:pt-32 sm:gap-48 pb-40">
          <h1 className="text-3xl font-bold mb-6">Contact Us</h1>
          <p className="text-sm text-muted-foreground mb-10">
            We’d love to hear from you. Reach out with questions, feedback, or collaboration opportunities.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
            {/* Contact Information */}
            <div className="space-y-6">
              <h2 className="text-xl font-semibold">Get in Touch</h2>
              <p>
                <b>Recommended:</b> For general inquiries, suggestions, or support, please email us directly at:
              </p>
              <p className="font-medium">
                <a
                  href="mailto:reach.saad@outlook.com"
                  className="text-primary underline"
                >
                  reach.saad@outlook.com
                </a>
              </p>


            </div>

            {/* Contact Form (dummy for prototype) */}
            <div>
              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1" htmlFor="name">
                    Name
                  </label>
                  <input
                    id="name"
                    type="text"
                    placeholder="Your Name"
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1" htmlFor="email">
                    Email
                  </label>
                  <input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1" htmlFor="message">
                    Message
                  </label>
                  <textarea
                    id="message"
                    rows={4}
                    placeholder="Write your message..."
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  />
                </div>

                <button
                  type="submit"
                  className="rounded-md bg-primary px-4 py-2 text-white font-medium shadow hover:bg-primary/90"
                >
                  Send Message
                </button>
              </form>
            </div>
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
