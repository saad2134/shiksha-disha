import Footer from "@/components/sections/footer/default";
import Navbar from "@/components/sections/navbar/default";
import Glow from "@/components/ui/glow";

export const metadata = {
  title: "Our Team | ShikshaDisha",
  description:
    "Meet the DevBandits team behind ShikshaDisha, working to provide personalized roadmaps for future-ready skills.",
};

const teamMembers = [
  {
    name: "Mohammed Abdul Mugees",
    role: "💼 Solutions Engineer",
    github: "https://github.com/mug3es",
  },
  {
    name: "Safaa Mujahid Khan",
    role: "🎨 UI/UX Designer",
    github: "https://github.com/SafaaMujahid05",
  },
  {
    name: "Fareed Ahmed Owais",
    role: "🎯 Team Lead",
    github: "https://github.com/FareedAhmedOwais",
  },
  {
    name: "Mohammed Saad Uddin",
    role: "🚀 Full-stack + AI/ML Developer",
    github: "https://github.com/saad2134",
  },
  {
    name: "Mohammed Abdul Rahman",
    role: "🖼️ Front-end Developer",
    github: "https://github.com/Abdul-Rahman26",
  },
  {
    name: "Abdur Rahman Qasim",
    role: "🔎 Research Engineer",
    github: "https://github.com/Abdur-rahman-01",
  },
];

export default function Team() {
  return (
    <>
      <main className="min-h-screen w-full overflow-hidden bg-background text-foreground">
        
        <Navbar />

        <section className="mx-auto max-w-4xl px-12 py-12 pt-32 md:pt-32">
          <h1 className="text-3xl font-bold mb-6">Our Smart India Hackathon 2025 Team</h1>
          <p className="text-sm text-muted-foreground mb-10">
            Meet <strong>DevBandits</strong>, the talented team driving ShikshaDisha forward.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
            {teamMembers.map((member, idx) => (
              <div
                key={idx}
                className="relative group border border-border rounded-lg p-6 flex flex-col items-start gap-2 hover:shadow-lg transition-shadow overflow-hidden"
              >
                {/* Glow background */}
                <div className="absolute top-0 left-0 h-full w-full translate-y-[1rem] opacity-80 transition-all duration-500 ease-in-out group-hover:translate-y-[-2rem] group-hover:opacity-100 pointer-events-none">
                  <Glow variant="bottom" />
                </div>

                {/* Content on top of Glow */}
                <h2 className="text-xl font-semibold relative z-10">{member.name}</h2>
                <p className="text-sm relative z-10">{member.role}</p>
                <a
                  href={member.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary underline text-sm mt-2 relative z-10"
                >
                  GitHub Profile
                </a>
              </div>
            ))}
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
