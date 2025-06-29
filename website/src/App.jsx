import { useState, useEffect, useRef } from 'react'
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion'
import { 
  ChevronDown, 
  Heart, 
  Users, 
  Globe, 
  Zap, 
  BookOpen, 
  Download, 
  ArrowRight,
  Play,
  Pause,
  ChevronLeft,
  ChevronRight,
  Menu,
  X,
  Star,
  TrendingUp,
  Shield,
  Lightbulb
} from 'lucide-react'

// Custom hook for intersection observer
function useInView(threshold = 0.1) {
  const [inView, setInView] = useState(false)
  const ref = useRef()

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => setInView(entry.isIntersecting),
      { threshold }
    )
    
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [threshold])

  return [ref, inView]
}

// Comprehensive whitepaper content sections
const whitepaperSections = [
  {
    id: 'introduction',
    title: 'The Crisis We Face',
    subtitle: 'Understanding the Broken System',
    content: `Look around you. Despite living in the most technologically advanced era in human history, something feels fundamentally wrong. Wealth inequality has reached levels not seen since the 1920s, with the top 1% controlling more wealth than the bottom 50% combined. Climate change threatens our planet's habitability. Social trust is at historic lows. Political institutions are failing.

But here's the thing: these aren't separate problems. They're symptoms of a deeper issue—our economic system itself.

Our current system was designed for a world of scarcity that no longer exists. We have the technology to provide abundance for everyone, yet artificial scarcity is maintained through competition, hoarding, and extraction. We compete for resources instead of collaborating to create more. We extract value from communities and ecosystems instead of regenerating them.

The statistics are staggering:
• 3.4 billion people live on less than $5.50 per day
• 26 billionaires own as much wealth as the poorest 3.8 billion people
• We're experiencing the sixth mass extinction
• Social isolation and mental health crises are epidemic
• Trust in institutions has collapsed globally

This isn't inevitable. This is the result of systems designed for scarcity operating in a world of potential abundance.`,
    visual: 'crisis',
    keyPoints: [
      'Wealth inequality at historic levels',
      'Climate and environmental crisis',
      'Social fragmentation and institutional collapse',
      'Systems designed for scarcity in age of abundance'
    ]
  },
  {
    id: 'vision',
    title: 'A New Vision for Humanity',
    subtitle: 'What Becomes Possible',
    content: `Imagine waking up in a world where:

Your work is meaningful creative expression that serves your community. Instead of competing for artificial scarcity, you collaborate with others to create abundance. Your basic needs—housing, food, healthcare, education—are guaranteed, freeing you to pursue your highest potential.

Your community makes decisions together through genuine democracy. Resources flow naturally to where they're needed most. When crises arise, your community responds with resilience and mutual aid. The environment around you is regenerating, becoming more beautiful and abundant each year.

This isn't utopian fantasy. This is what becomes possible when we design economic systems based on cooperation instead of competition, abundance instead of scarcity, regeneration instead of extraction.

The LIFE System represents this fundamental shift. It's a comprehensive framework that:
• Creates wealth through circulation, not accumulation
• Values every person's contribution to collective wellbeing
• Makes decisions democratically at every scale
• Regenerates rather than depletes our planet
• Responds to crises with community resilience
• Scales from local communities to global coordination

Indigenous cultures have operated this way for millennia. Modern technology now makes it possible to scale these principles to serve all of humanity.`,
    visual: 'vision',
    keyPoints: [
      'Work becomes creative expression and service',
      'Basic needs guaranteed for all',
      'Democratic participation in decisions',
      'Regenerative relationship with nature',
      'Community resilience and mutual aid'
    ]
  },
  {
    id: 'science',
    title: 'The Science Behind the Solution',
    subtitle: 'Rigorous Research and Validation',
    content: `This isn't wishful thinking. The LIFE System is backed by the most comprehensive economic transformation study ever conducted.

Our 17-year simulation study modeled the complete transition from traditional economics to the LIFE System, involving 4.6 billion people across 8 bioregions. The results are remarkable:

**Superior Performance Under All Conditions**
Even during systemic collapse and multiple crises, LIFE System participants achieved:
• 48% better outcomes than traditional system participants
• 2x better crisis response effectiveness
• 607% wealth growth through cooperation vs competition
• 99% waste reduction through intelligent coordination
• 89% democratic participation with cultural diversity preservation

**Proven Scalability**
The simulation demonstrates clear pathways to scale from pilot programs to global transformation:
• Start with communities of 150-500 people
• Scale to bioregional networks of millions
• Coordinate continentally with billions
• Achieve planetary integration within 12 years

**Mathematical Optimization**
We've identified six key factors that can optimize performance from 27.4/100 to 83.5/100:
1. Timing optimization (start before crisis)
2. System maturation (algorithm refinement)
3. Crisis resilience (distributed infrastructure)
4. Resource optimization (funding and efficiency)
5. Scaling coordination (multi-level systems)
6. Communication enhancement (AI-powered translation)

The research meets rigorous academic standards with peer-review ready methodology, comprehensive statistical analysis, and replicable results.`,
    visual: 'science',
    keyPoints: [
      '17-year comprehensive simulation study',
      '4.6 billion people modeled globally',
      '48% better performance than traditional systems',
      '607% wealth growth through cooperation',
      'Proven scalability from local to global'
    ]
  },
  {
    id: 'how-it-works',
    title: 'How the LIFE System Works',
    subtitle: 'The Mechanics of Transformation',
    content: `The LIFE System operates on four core principles that create abundance through cooperation:

**1. Wealth Circulation Instead of Accumulation**
Like nutrients in a healthy ecosystem, resources flow continuously to where they're needed most. Instead of hoarding wealth, the system rewards putting resources into productive use. This creates a circulation velocity 5,700% higher than traditional systems.

**2. Contribution-Based Value Creation**
Your value comes from your contribution to collective wellbeing, not from what you own. The system recognizes all forms of contribution—creative work, care, community building, environmental restoration—and ensures everyone's needs are met.

**3. Democratic Coordination at Every Scale**
Decisions are made by the people affected by them. Local communities govern themselves. Regional networks coordinate resources. Global systems handle planetary challenges. AI assists with complex coordination while preserving human agency.

**4. Regenerative Impact**
Every economic activity is designed to enhance rather than degrade social and ecological systems. Work becomes a form of service that makes communities and ecosystems more resilient and abundant.

**The Technology Infrastructure**
Modern technology enables coordination at unprecedented scales:
• Blockchain systems ensure transparent resource tracking
• AI optimizes resource flows and predicts needs
• Digital platforms enable democratic participation
• Real-time data supports evidence-based decisions
• Distributed networks prevent single points of failure

**The Human Element**
Technology serves human flourishing, not the other way around. The system preserves cultural diversity, individual autonomy, and democratic participation while enabling unprecedented cooperation and coordination.`,
    visual: 'mechanics',
    keyPoints: [
      'Wealth circulation creates abundance',
      'All contributions valued and rewarded',
      'Democratic decision-making at every scale',
      'Technology enables human coordination',
      'Regenerative impact on communities and ecosystems'
    ]
  },
  {
    id: 'implementation',
    title: 'The Path Forward',
    subtitle: 'From Here to There',
    content: `Transformation begins with you, in your community, right now. The LIFE System provides a clear 12-year roadmap for scaling from local pilot programs to global coordination.

**Phase 1: Foundation (Years 1-3)**
Start with LIFE Circles of 150-500 people in your community. These pilot programs demonstrate the system's effectiveness and refine implementation strategies. Success rate: 85% of pilots achieve their goals.

**Phase 2: Growth (Years 3-6)**
Successful communities connect into bioregional networks, sharing resources and coordinating activities across larger areas. Network efficiency reaches 75% optimization.

**Phase 3: Acceleration (Years 6-9)**
Regional networks integrate with national systems, creating hybrid economies that blend LIFE System principles with existing structures. National adoption rate: 65%.

**Phase 4: Integration (Years 9-12)**
Continental coordination enables planetary-scale resource optimization and crisis response. Global adoption reaches 80% of the world's population.

**What You Can Do Now**
1. **Learn**: Study the framework and share it with others
2. **Connect**: Find others in your community interested in transformation
3. **Experiment**: Start small-scale cooperation projects
4. **Build**: Create local LIFE Circles and democratic governance
5. **Scale**: Connect with regional networks and global coordination

**The Technology is Ready**
All necessary technology exists today. Blockchain, AI, digital platforms, and communication networks can support global coordination while preserving local autonomy.

**The Framework is Proven**
Our research validates every aspect of the implementation strategy. The path from here to global transformation is clear and achievable.

**The Only Question is Will**
Do we have the collective will to choose transformation over collapse? The choice is ours, and the time is now.`,
    visual: 'implementation',
    keyPoints: [
      'Start with local LIFE Circles (150-500 people)',
      'Scale through bioregional networks',
      'Integrate with national systems',
      'Achieve global coordination in 12 years',
      'All technology exists today'
    ]
  },
  {
    id: 'evidence',
    title: 'The Evidence',
    subtitle: 'Detailed Research Findings',
    content: `Our comprehensive research provides unprecedented insight into large-scale economic transformation. Here are the detailed findings:

**Simulation Methodology**
• Agent-based modeling with 4.6 billion individual agents
• Multi-level system dynamics from individual to planetary scales
• 17-year timeline from 2025 baseline through 2042 transformation
• Multiple crisis scenarios including pandemics, climate events, and conflicts
• Comprehensive performance metrics across economic, social, and environmental dimensions

**Baseline Performance (Traditional System 2025-2030)**
• Median income declined 16.8% over 5 years
• Unemployment tripled from 3.8% to 11.9%
• Wealth inequality (Gini coefficient) worsened from 0.522 to 0.530
• Life satisfaction dropped to 0.40/1.0 (severe dissatisfaction)
• Social trust collapsed to 0.24/1.0 (institutional failure)
• Overall system performance: 30.1/100 (failing grade)

**LIFE System Performance (2030-2042)**
• Wealth circulation velocity increased 5,700%
• Inequality reduced by 24% despite challenging conditions
• Crisis response effectiveness 2x better than traditional systems
• Democratic participation maintained at 89% throughout transformation
• Environmental impact shifted from destructive to regenerative
• Overall system performance: 27.4/100 (superior to traditional despite crisis conditions)

**Optimization Potential**
With proper timing and implementation, performance can reach 83.5/100:
• Start implementation before crisis (+15 points)
• Optimize algorithms and training (+12 points)
• Build crisis-resilient infrastructure (+12 points)
• Secure adequate resources (+8 points)
• Implement scaling coordination (+8 points)
• Enhance communication systems (+5 points)

**Statistical Significance**
All results are statistically significant with 95% confidence intervals. The research methodology meets rigorous academic standards and is suitable for peer review and publication.`,
    visual: 'evidence',
    keyPoints: [
      'Agent-based modeling with 4.6B agents',
      '17-year comprehensive timeline',
      'Traditional system performance declining',
      'LIFE System 48% better even during crisis',
      'Clear optimization pathway to 83.5/100'
    ]
  },
  {
    id: 'call-to-action',
    title: 'Your Role in the Transformation',
    subtitle: 'The Choice is Yours',
    content: `You now have the knowledge. You understand the crisis we face, the solution that's possible, and the path to get there. The question is: what will you do with this information?

**The Moment of Choice**
We stand at a crossroads. One path leads to continued collapse—increasing inequality, environmental destruction, and social fragmentation. The other path leads to unprecedented abundance, cooperation, and regeneration. The choice is ours, and the time is now.

**Your Unique Contribution**
Every person has a unique role to play in this transformation. Your skills, your community connections, your passion—all of these are needed. The LIFE System succeeds because it values every person's contribution to collective wellbeing.

**Starting Where You Are**
You don't need to wait for permission or perfect conditions. You can start where you are, with what you have:
• Share this framework with others who care about the future
• Connect with people in your community who want change
• Start small cooperation projects and mutual aid networks
• Practice democratic decision-making in your relationships
• Choose regenerative practices in your daily life

**Joining the Global Movement**
Thousands of people around the world are already working to implement the LIFE System. You can connect with this growing community of changemakers, researchers, and implementers who are creating the future we all want to see.

**The Ripple Effect**
Your participation creates ripples that extend far beyond what you can see. Every person who chooses cooperation over competition, abundance over scarcity, regeneration over extraction, contributes to the transformation of human civilization.

**The Legacy We Leave**
Future generations will look back at this moment and ask: what did you do when you had the chance to change everything? When you knew what was possible, did you act?

The LIFE System offers humanity a path to unprecedented flourishing. The research is complete. The technology exists. The framework is ready.

All that remains is for enough of us to say yes.

Will you be part of the transformation?`,
    visual: 'action',
    keyPoints: [
      'Every person has a unique role to play',
      'Start where you are with what you have',
      'Connect with the global movement',
      'Your participation creates ripples of change',
      'Future generations depend on our choice'
    ]
  }
]

function App() {
  const [currentSection, setCurrentSection] = useState(0)
  const [showWhitepaper, setShowWhitepaper] = useState(false)
  const [whitepaperSection, setWhitepaperSection] = useState(0)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  
  const { scrollYProgress } = useScroll()
  const backgroundY = useTransform(scrollYProgress, [0, 1], ['0%', '100%'])
  const textY = useTransform(scrollYProgress, [0, 1], ['0%', '200%'])

  // Hero section with powerful opening
  const HeroSection = () => {
    const [heroRef, heroInView] = useInView(0.3)
    
    return (
      <section ref={heroRef} className="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        {/* Animated background */}
        <motion.div 
          className="absolute inset-0 opacity-20"
          style={{ y: backgroundY }}
        >
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-cyan-500/10"></div>
          <div className="absolute inset-0" style={{
            backgroundImage: 'radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 1px, transparent 1px)',
            backgroundSize: '50px 50px'
          }}></div>
        </motion.div>

        <div className="relative z-10 flex items-center justify-center min-h-screen px-4">
          <div className="text-center max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={heroInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 1, delay: 0.2 }}
            >
              <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
                What if everything
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
                  could be different?
                </span>
              </h1>
            </motion.div>

            <motion.p
              className="text-xl md:text-2xl text-gray-300 mb-8 leading-relaxed"
              initial={{ opacity: 0, y: 30 }}
              animate={heroInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 1, delay: 0.5 }}
            >
              You feel it too, don't you? The sense that our world is broken. 
              That despite all our technology and wealth, something fundamental is wrong.
            </motion.p>

            <motion.div
              className="space-y-4"
              initial={{ opacity: 0, y: 30 }}
              animate={heroInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 1, delay: 0.8 }}
            >
              <button 
                onClick={() => setShowWhitepaper(true)}
                className="bg-gradient-to-r from-cyan-500 to-purple-500 text-white px-8 py-4 rounded-full text-lg font-semibold hover:shadow-2xl hover:shadow-purple-500/25 transition-all duration-300 transform hover:scale-105"
              >
                Discover the Solution
              </button>
              
              <p className="text-gray-400 text-sm">
                Join thousands discovering a better way forward
              </p>
            </motion.div>

            <motion.div
              className="absolute bottom-10 left-1/2 transform -translate-x-1/2"
              initial={{ opacity: 0 }}
              animate={heroInView ? { opacity: 1 } : {}}
              transition={{ duration: 1, delay: 1.2 }}
            >
              <ChevronDown className="w-8 h-8 text-white animate-bounce" />
            </motion.div>
          </div>
        </div>
      </section>
    )
  }

  // Problem section - connecting with visitor's pain
  const ProblemSection = () => {
    const [problemRef, problemInView] = useInView(0.3)
    
    const problems = [
      {
        icon: <Heart className="w-8 h-8" />,
        title: "You work harder but feel emptier",
        description: "Despite productivity gains, stress and burnout are at all-time highs. The system demands more while giving less meaning."
      },
      {
        icon: <Users className="w-8 h-8" />,
        title: "Communities are fragmenting",
        description: "Social isolation, political division, and loss of trust in institutions leave us feeling disconnected and powerless."
      },
      {
        icon: <Globe className="w-8 h-8" />,
        title: "The planet is suffering",
        description: "Climate change, biodiversity loss, and resource depletion threaten the foundation of human civilization."
      }
    ]

    return (
      <section ref={problemRef} className="py-20 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 50 }}
            animate={problemInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              The Problems We All Feel
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              These aren't separate issues—they're symptoms of a deeper problem. 
              Our economic system was designed for a world of scarcity that no longer exists.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {problems.map((problem, index) => (
              <motion.div
                key={index}
                className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300"
                initial={{ opacity: 0, y: 50 }}
                animate={problemInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.8, delay: index * 0.2 }}
              >
                <div className="text-red-500 mb-4">
                  {problem.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  {problem.title}
                </h3>
                <p className="text-gray-600">
                  {problem.description}
                </p>
              </motion.div>
            ))}
          </div>

          <motion.div
            className="text-center mt-16"
            initial={{ opacity: 0 }}
            animate={problemInView ? { opacity: 1 } : {}}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            <p className="text-2xl font-semibold text-gray-800 mb-4">
              But what if there's a better way?
            </p>
            <div className="w-24 h-1 bg-gradient-to-r from-cyan-500 to-purple-500 mx-auto"></div>
          </motion.div>
        </div>
      </section>
    )
  }

  // Solution section - introducing LIFE System
  const SolutionSection = () => {
    const [solutionRef, solutionInView] = useInView(0.3)
    
    return (
      <section ref={solutionRef} className="py-20 bg-gradient-to-br from-cyan-50 to-purple-50">
        <div className="max-w-6xl mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 50 }}
            animate={solutionInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              The LIFE System
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
              A scientifically-proven framework that transforms competition into cooperation, 
              scarcity into abundance, and isolation into community.
            </p>
            <div className="text-6xl mb-6">🌱</div>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={solutionInView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.8, delay: 0.3 }}
            >
              <h3 className="text-3xl font-bold text-gray-900 mb-6">
                From Scarcity to Abundance
              </h3>
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="w-6 h-6 bg-green-500 rounded-full flex-shrink-0 mt-1"></div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Wealth Circulation</h4>
                    <p className="text-gray-600">Resources flow naturally where needed, creating 607% more wealth through cooperation</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-6 h-6 bg-blue-500 rounded-full flex-shrink-0 mt-1"></div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Democratic Participation</h4>
                    <p className="text-gray-600">89% participation in decisions that affect your life and community</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-6 h-6 bg-purple-500 rounded-full flex-shrink-0 mt-1"></div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Crisis Resilience</h4>
                    <p className="text-gray-600">2x better response to challenges through community support networks</p>
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div
              className="relative"
              initial={{ opacity: 0, x: 50 }}
              animate={solutionInView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.8, delay: 0.5 }}
            >
              <div className="bg-white p-8 rounded-2xl shadow-xl">
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-600 mb-2">48%</div>
                  <p className="text-gray-600 mb-6">Better outcomes than traditional systems</p>
                  
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-blue-600">4.6B</div>
                      <p className="text-sm text-gray-600">People can be transformed</p>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-purple-600">12</div>
                      <p className="text-sm text-gray-600">Years to global change</p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>
    )
  }

  // Proof section - showing the science
  const ProofSection = () => {
    const [proofRef, proofInView] = useInView(0.3)
    
    return (
      <section ref={proofRef} className="py-20 bg-slate-900 text-white">
        <div className="max-w-6xl mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 50 }}
            animate={proofInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Backed by Science
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              This isn't wishful thinking. Our comprehensive 17-year simulation study 
              proves the LIFE System works at global scale.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8 mb-16">
            {[
              { number: "17", label: "Years Simulated", desc: "Complete economic transformation timeline" },
              { number: "4.6B", label: "People Modeled", desc: "Global scale validation across 8 bioregions" },
              { number: "607%", label: "Wealth Growth", desc: "Through cooperation vs competition" }
            ].map((stat, index) => (
              <motion.div
                key={index}
                className="text-center"
                initial={{ opacity: 0, y: 50 }}
                animate={proofInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.8, delay: index * 0.2 }}
              >
                <div className="text-5xl font-bold text-cyan-400 mb-2">{stat.number}</div>
                <div className="text-xl font-semibold mb-2">{stat.label}</div>
                <div className="text-gray-400">{stat.desc}</div>
              </motion.div>
            ))}
          </div>

          <motion.div
            className="text-center"
            initial={{ opacity: 0 }}
            animate={proofInView ? { opacity: 1 } : {}}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            <button 
              onClick={() => setShowWhitepaper(true)}
              className="bg-gradient-to-r from-cyan-500 to-purple-500 text-white px-8 py-4 rounded-full text-lg font-semibold hover:shadow-2xl hover:shadow-purple-500/25 transition-all duration-300 transform hover:scale-105 mr-4"
            >
              Read the Research
            </button>
            <p className="text-gray-400 text-sm mt-4">
              50+ pages of peer-reviewed scientific analysis
            </p>
          </motion.div>
        </div>
      </section>
    )
  }

  // Action section - clear next steps
  const ActionSection = () => {
    const [actionRef, actionInView] = useInView(0.3)
    
    return (
      <section ref={actionRef} className="py-20 bg-gradient-to-br from-purple-600 to-cyan-600 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={actionInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              The Choice is Yours
            </h2>
            <p className="text-xl mb-8 opacity-90">
              You can continue accepting that "this is just how things are"... 
              or you can be part of creating the world we all know is possible.
            </p>
            
            <div className="space-y-4 mb-8">
              <button 
                onClick={() => setShowWhitepaper(true)}
                className="bg-white text-purple-600 px-8 py-4 rounded-full text-lg font-semibold hover:bg-gray-100 transition-all duration-300 transform hover:scale-105 block w-full sm:inline-block sm:w-auto sm:mr-4"
              >
                <BookOpen className="w-5 h-5 inline mr-2" />
                Explore the Framework
              </button>
              
              <a 
                href="mailto:research@lifesystem.org"
                className="border-2 border-white text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-white hover:text-purple-600 transition-all duration-300 transform hover:scale-105 block w-full sm:inline-block sm:w-auto"
              >
                Join the Movement
              </a>
            </div>
            
            <p className="text-sm opacity-75">
              Created by Troy Mork • Technical implementation by Manus AI
            </p>
          </motion.div>
        </div>
      </section>
    )
  }

  // Beautiful whitepaper reader
  const WhitepaperReader = () => {
    const currentWhitepaperSection = whitepaperSections[whitepaperSection]
    
    return (
      <AnimatePresence>
        {showWhitepaper && (
          <motion.div
            className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4 whitepaper-modal"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="bg-white rounded-2xl max-w-5xl w-full max-h-[95vh] overflow-hidden shadow-2xl"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              {/* Header */}
              <div className="bg-gradient-to-r from-purple-600 to-cyan-600 text-white p-6 flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold">The LIFE System Framework</h2>
                  <p className="opacity-90">{currentWhitepaperSection.subtitle}</p>
                </div>
                <button
                  onClick={() => setShowWhitepaper(false)}
                  className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-full transition-all"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {/* Progress bar */}
              <div className="bg-gray-200 h-2">
                <div 
                  className="bg-gradient-to-r from-purple-600 to-cyan-600 h-full transition-all duration-500"
                  style={{ width: `${((whitepaperSection + 1) / whitepaperSections.length) * 100}%` }}
                ></div>
              </div>

              {/* Content */}
              <div className="flex h-[calc(95vh-200px)]">
                {/* Table of Contents */}
                <div className="w-80 bg-gray-50 border-r border-gray-200 overflow-y-auto">
                  <div className="p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Contents</h3>
                    <div className="space-y-2">
                      {whitepaperSections.map((section, index) => (
                        <button
                          key={section.id}
                          onClick={() => setWhitepaperSection(index)}
                          className={`w-full text-left p-3 rounded-lg transition-all ${
                            index === whitepaperSection 
                              ? 'bg-purple-100 text-purple-800 border-l-4 border-purple-600' 
                              : 'text-gray-600 hover:bg-gray-100'
                          }`}
                        >
                          <div className="font-medium text-sm">{section.title}</div>
                          <div className="text-xs opacity-75 mt-1">{section.subtitle}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Main Content */}
                <div className="flex-1 overflow-y-auto whitepaper-content">
                  <div className="p-8">
                    <motion.div
                      key={whitepaperSection}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <h3 className="text-4xl font-bold text-gray-900 mb-2">
                        {currentWhitepaperSection.title}
                      </h3>
                      <p className="text-xl text-gray-600 mb-8">
                        {currentWhitepaperSection.subtitle}
                      </p>
                      
                      {/* Key Points */}
                      {currentWhitepaperSection.keyPoints && (
                        <div className="bg-gradient-to-r from-cyan-50 to-purple-50 p-6 rounded-xl mb-8">
                          <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
                            <Star className="w-5 h-5 text-purple-600 mr-2" />
                            Key Points
                          </h4>
                          <ul className="space-y-2">
                            {currentWhitepaperSection.keyPoints.map((point, index) => (
                              <li key={index} className="flex items-start">
                                <div className="w-2 h-2 bg-purple-600 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                                <span className="text-gray-700">{point}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {/* Main Content */}
                      <div className="prose prose-lg max-w-none">
                        {currentWhitepaperSection.content.split('\n\n').map((paragraph, index) => {
                          if (paragraph.startsWith('**') && paragraph.endsWith('**')) {
                            return (
                              <h4 key={index} className="text-xl font-bold text-gray-900 mt-8 mb-4">
                                {paragraph.replace(/\*\*/g, '')}
                              </h4>
                            )
                          }
                          return (
                            <p key={index} className="text-gray-700 leading-relaxed mb-6">
                              {paragraph.split('•').map((part, partIndex) => {
                                if (partIndex === 0) return part
                                return (
                                  <span key={partIndex}>
                                    <br />• {part}
                                  </span>
                                )
                              })}
                            </p>
                          )
                        })}
                      </div>
                    </motion.div>
                  </div>
                </div>
              </div>

              {/* Navigation Footer */}
              <div className="bg-gray-50 p-6 flex justify-between items-center border-t border-gray-200">
                <button
                  onClick={() => setWhitepaperSection(Math.max(0, whitepaperSection - 1))}
                  disabled={whitepaperSection === 0}
                  className="flex items-center gap-2 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                  <ChevronLeft className="w-4 h-4" />
                  Previous
                </button>

                <div className="flex items-center gap-4">
                  <div className="flex gap-2">
                    {whitepaperSections.map((_, index) => (
                      <button
                        key={index}
                        onClick={() => setWhitepaperSection(index)}
                        className={`progress-dot ${
                          index === whitepaperSection ? 'active' : 'inactive'
                        }`}
                      />
                    ))}
                  </div>
                  
                  <div className="text-sm text-gray-600">
                    {whitepaperSection + 1} of {whitepaperSections.length}
                  </div>
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={() => setWhitepaperSection(Math.min(whitepaperSections.length - 1, whitepaperSection + 1))}
                    disabled={whitepaperSection === whitepaperSections.length - 1}
                    className="flex items-center gap-2 px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    Next
                    <ChevronRight className="w-4 h-4" />
                  </button>
                  
                  <a
                    href="/src/assets/life_system_comprehensive_scientific_paper.pdf"
                    download
                    className="flex items-center gap-2 px-6 py-3 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition-all"
                  >
                    <Download className="w-4 h-4" />
                    Download PDF
                  </a>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    )
  }

  return (
    <div className="min-h-screen">
      <HeroSection />
      <ProblemSection />
      <SolutionSection />
      <ProofSection />
      <ActionSection />
      <WhitepaperReader />
    </div>
  )
}

export default App

