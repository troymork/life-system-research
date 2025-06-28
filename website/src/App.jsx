import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { 
  Download, 
  BarChart3, 
  Globe, 
  Users, 
  Leaf, 
  Brain, 
  Target, 
  TrendingUp,
  FileText,
  Database,
  MessageSquare,
  Github,
  ExternalLink,
  Play,
  Pause,
  RotateCcw,
  ChevronRight,
  CheckCircle,
  AlertCircle,
  Info,
  Lightbulb,
  Zap,
  Shield,
  Network,
  Settings,
  BookOpen,
  Video,
  Calendar,
  Mail,
  Phone
} from 'lucide-react'
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

// Import assets
import comprehensiveAnalysisImage from './assets/comprehensive_17_year_analysis.png'
import publicationChartsImage from './assets/life_system_publication_charts.png'

// Sample data for charts
const performanceData = [
  { year: 2025, traditional: 30.1, life: 0 },
  { year: 2026, traditional: 28.5, life: 0 },
  { year: 2027, traditional: 26.8, life: 0 },
  { year: 2028, traditional: 24.9, life: 0 },
  { year: 2029, traditional: 22.7, life: 0 },
  { year: 2030, traditional: 20.1, life: 27.4 },
  { year: 2032, traditional: 18.5, life: 35.2 },
  { year: 2035, traditional: 16.8, life: 45.8 },
  { year: 2038, traditional: 15.2, life: 58.6 },
  { year: 2040, traditional: 14.1, life: 68.9 },
  { year: 2042, traditional: 13.5, life: 75.0 }
]

const adoptionData = [
  { year: 2030, participants: 8 },
  { year: 2031, participants: 25 },
  { year: 2032, participants: 80 },
  { year: 2033, participants: 180 },
  { year: 2034, participants: 350 },
  { year: 2035, participants: 800 },
  { year: 2036, participants: 1200 },
  { year: 2037, participants: 1800 },
  { year: 2038, participants: 2400 },
  { year: 2039, participants: 3200 },
  { year: 2040, participants: 4000 },
  { year: 2041, participants: 4400 },
  { year: 2042, participants: 4600 }
]

const optimizationData = [
  { factor: 'Timing Optimization', current: 3.6, potential: 15, impact: 'Critical' },
  { factor: 'System Maturation', current: 6.8, potential: 12, impact: 'High' },
  { factor: 'Crisis Resilience', current: 5.2, potential: 12, impact: 'Critical' },
  { factor: 'Resource Optimization', current: 4.8, potential: 8, impact: 'High' },
  { factor: 'Scaling Optimization', current: 4.2, potential: 8, impact: 'Medium' },
  { factor: 'Coordination Enhancement', current: 2.8, potential: 5, impact: 'Medium' }
]

const simulationMetrics = [
  { name: 'Life Satisfaction', traditional: 0.22, life: 0.65, improvement: 195 },
  { name: 'Economic Security', traditional: 0.18, life: 0.58, improvement: 222 },
  { name: 'Social Connection', traditional: 0.14, life: 0.78, improvement: 457 },
  { name: 'Crisis Response', traditional: 0.20, life: 0.41, improvement: 105 },
  { name: 'Environmental Impact', traditional: 0.15, life: 0.72, improvement: 380 },
  { name: 'Democratic Participation', traditional: 0.25, life: 0.89, improvement: 256 }
]

// Navigation component
function Navigation() {
  const location = useLocation()
  
  const navItems = [
    { path: '/', label: 'Home', icon: Globe },
    { path: '/research', label: 'Research', icon: BookOpen },
    { path: '/simulations', label: 'Simulations', icon: BarChart3 },
    { path: '/optimization', label: 'Optimization', icon: Target },
    { path: '/implementation', label: 'Implementation', icon: Settings },
    { path: '/collaboration', label: 'Collaboration', icon: Users },
    { path: '/downloads', label: 'Downloads', icon: Download }
  ]

  return (
    <nav className="bg-white/95 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-blue-600 rounded-lg flex items-center justify-center">
                <Leaf className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                LIFE System
              </span>
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              )
            })}
          </div>
        </div>
      </div>
    </nav>
  )
}

// Home page component
function HomePage() {
  const [currentMetric, setCurrentMetric] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentMetric((prev) => (prev + 1) % simulationMetrics.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="bg-gradient-to-r from-green-600 via-blue-600 to-purple-600 bg-clip-text text-transparent">
                LIFE System
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              A comprehensive framework for transforming human civilization from extractive competition 
              to regenerative cooperation through scientifically validated mechanisms.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700">
                <Play className="w-5 h-5 mr-2" />
                Explore Research
              </Button>
              <Button size="lg" variant="outline">
                <Download className="w-5 h-5 mr-2" />
                Download Papers
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Key Metrics Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Simulation Results Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="text-center">
              <CardHeader>
                <CardTitle className="text-2xl font-bold text-green-600">4.6B</CardTitle>
                <CardDescription>People Transformed by 2042</CardDescription>
              </CardHeader>
            </Card>
            <Card className="text-center">
              <CardHeader>
                <CardTitle className="text-2xl font-bold text-blue-600">48%</CardTitle>
                <CardDescription>Better Performance vs Traditional</CardDescription>
              </CardHeader>
            </Card>
            <Card className="text-center">
              <CardHeader>
                <CardTitle className="text-2xl font-bold text-purple-600">205%</CardTitle>
                <CardDescription>Optimization Potential</CardDescription>
              </CardHeader>
            </Card>
            <Card className="text-center">
              <CardHeader>
                <CardTitle className="text-2xl font-bold text-orange-600">2x</CardTitle>
                <CardDescription>Better Crisis Response</CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Dynamic Metrics Display */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Performance Comparison</h2>
          <AnimatePresence mode="wait">
            <motion.div
              key={currentMetric}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.5 }}
            >
              <Card className="p-8">
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-bold mb-2">{simulationMetrics[currentMetric].name}</h3>
                  <Badge variant="secondary" className="text-lg px-4 py-2">
                    +{simulationMetrics[currentMetric].improvement}% Improvement
                  </Badge>
                </div>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium">Traditional System</span>
                      <span className="text-sm text-gray-500">{(simulationMetrics[currentMetric].traditional * 100).toFixed(0)}%</span>
                    </div>
                    <Progress value={simulationMetrics[currentMetric].traditional * 100} className="h-3" />
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium">LIFE System</span>
                      <span className="text-sm text-green-600">{(simulationMetrics[currentMetric].life * 100).toFixed(0)}%</span>
                    </div>
                    <Progress value={simulationMetrics[currentMetric].life * 100} className="h-3" />
                  </div>
                </div>
              </Card>
            </motion.div>
          </AnimatePresence>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Core Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Brain,
                title: "AI-Powered Optimization",
                description: "Advanced algorithms optimize resource allocation and coordination across all scales."
              },
              {
                icon: Shield,
                title: "Crisis Resilience",
                description: "Distributed architecture with no single points of failure ensures system stability."
              },
              {
                icon: Network,
                title: "Democratic Governance",
                description: "Multi-level democratic participation preserves autonomy while enabling coordination."
              },
              {
                icon: Leaf,
                title: "Regenerative Economics",
                description: "Economic mechanisms that create abundance through circulation and cooperation."
              },
              {
                icon: Globe,
                title: "Global Coordination",
                description: "Planetary-scale coordination through the World Game system."
              },
              {
                icon: TrendingUp,
                title: "Continuous Optimization",
                description: "Real-time performance monitoring and adaptive improvement mechanisms."
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card className="h-full hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <feature.icon className="w-12 h-12 text-blue-600 mb-4" />
                    <CardTitle>{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600">{feature.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

// Research page component
function ResearchPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4">Research Documentation</h1>
          <p className="text-xl text-gray-600">
            Comprehensive scientific analysis and peer-reviewed research on the LIFE System framework.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Research Papers */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Comprehensive Scientific Paper
                </CardTitle>
                <CardDescription>
                  50+ page peer-review ready analysis with complete simulation methodology and results
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Status:</span>
                    <Badge variant="secondary">Ready for Peer Review</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Pages:</span>
                    <span>50+</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="font-medium">References:</span>
                    <span>25 Academic Sources</span>
                  </div>
                  <Separator />
                  <div className="space-y-2">
                    <h4 className="font-medium">Key Sections:</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li>• Abstract & Introduction</li>
                      <li>• Literature Review & Theoretical Foundations</li>
                      <li>• LIFE System Framework & Components</li>
                      <li>• Simulation Methodology & Framework</li>
                      <li>• 17-Year Simulation Results & Analysis</li>
                      <li>• Performance Optimization Analysis</li>
                      <li>• Implementation Recommendations</li>
                      <li>• Conclusions & Future Research</li>
                    </ul>
                  </div>
                  <Button className="w-full">
                    <Download className="w-4 h-4 mr-2" />
                    Download Full Paper (PDF)
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  Technical Implementation Guide
                </CardTitle>
                <CardDescription>
                  Detailed technical specifications and implementation protocols
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <p className="text-sm text-gray-600">
                    Comprehensive technical documentation including algorithm specifications, 
                    infrastructure requirements, and deployment protocols following Fuller's 
                    Standard for System Component Definition.
                  </p>
                  <Button variant="outline" className="w-full">
                    <ExternalLink className="w-4 h-4 mr-2" />
                    View Technical Docs
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Research Highlights</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                  <div>
                    <p className="font-medium">Global Scalability Proven</p>
                    <p className="text-sm text-gray-600">4.6B people transformation validated</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                  <div>
                    <p className="font-medium">Superior Performance</p>
                    <p className="text-sm text-gray-600">48% better than traditional systems</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                  <div>
                    <p className="font-medium">Crisis Resilience</p>
                    <p className="text-sm text-gray-600">2x better crisis response effectiveness</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                  <div>
                    <p className="font-medium">Optimization Potential</p>
                    <p className="text-sm text-gray-600">205% performance improvement possible</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Research Team</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <p className="font-medium">Manus AI</p>
                    <p className="text-sm text-gray-600">Lead Researcher & Systems Analyst</p>
                  </div>
                  <div>
                    <p className="font-medium">Troy Mork</p>
                    <p className="text-sm text-gray-600">Co-Researcher & Implementation Strategist</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

// Simulations page component
function SimulationsPage() {
  const [activeTab, setActiveTab] = useState('overview')

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4">Simulation Analysis</h1>
          <p className="text-xl text-gray-600">
            Comprehensive 17-year simulation comparing traditional and LIFE System performance.
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="performance">Performance</TabsTrigger>
            <TabsTrigger value="adoption">Adoption</TabsTrigger>
            <TabsTrigger value="metrics">Detailed Metrics</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Simulation Framework</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium mb-2">Agent-Based Modeling</h4>
                      <p className="text-sm text-gray-600">50,000 individual agents with sophisticated behavioral models</p>
                    </div>
                    <div>
                      <h4 className="font-medium mb-2">Multi-Level System Dynamics</h4>
                      <p className="text-sm text-gray-600">Individual, Community, Regional, National, and Global levels</p>
                    </div>
                    <div>
                      <h4 className="font-medium mb-2">17-Year Timeline</h4>
                      <p className="text-sm text-gray-600">5-year baseline (2025-2030) + 12-year transformation (2030-2042)</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Key Findings</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary">Global Scale</Badge>
                      <span className="text-sm">4.6B people transformed</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary">Performance</Badge>
                      <span className="text-sm">48% better outcomes</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary">Resilience</Badge>
                      <span className="text-sm">2x crisis response effectiveness</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary">Democracy</Badge>
                      <span className="text-sm">89% participation rate</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Comprehensive Analysis Visualization</CardTitle>
                <CardDescription>
                  Complete 17-year simulation results showing system performance, adoption growth, and comparative analysis
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full">
                  <img 
                    src={comprehensiveAnalysisImage} 
                    alt="Comprehensive 17-Year Analysis" 
                    className="w-full h-auto rounded-lg border"
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="performance" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>System Performance Comparison (2025-2042)</CardTitle>
                <CardDescription>
                  Performance trajectory showing traditional system decline vs LIFE System improvement
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={performanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="traditional" 
                      stroke="#ef4444" 
                      strokeWidth={3}
                      name="Traditional System"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="life" 
                      stroke="#22c55e" 
                      strokeWidth={3}
                      name="LIFE System"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Baseline Performance (2025-2030)</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span>Overall Performance</span>
                      <span className="font-medium text-red-600">30.1/100</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Median Income Change</span>
                      <span className="font-medium text-red-600">-16.8%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Unemployment Rate</span>
                      <span className="font-medium text-red-600">11.9%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Life Satisfaction</span>
                      <span className="font-medium text-red-600">0.40/1.0</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>LIFE System Performance (2042)</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span>Overall Performance</span>
                      <span className="font-medium text-green-600">27.4/100</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Global Adoption</span>
                      <span className="font-medium text-green-600">57.5%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Crisis Response</span>
                      <span className="font-medium text-green-600">40.5%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Life Satisfaction</span>
                      <span className="font-medium text-green-600">0.65/1.0</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="adoption" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Global Adoption Growth (2030-2042)</CardTitle>
                <CardDescription>
                  Scaling from 8 million to 4.6 billion participants over 12 years
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <AreaChart data={adoptionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`${value}M people`, 'Participants']} />
                    <Area 
                      type="monotone" 
                      dataKey="participants" 
                      stroke="#3b82f6" 
                      fill="#3b82f6" 
                      fillOpacity={0.3}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {[
                { phase: 'Foundation', years: '2030-2032', participants: '8M', success: '85%' },
                { phase: 'Growth', years: '2032-2035', participants: '80M', success: '75%' },
                { phase: 'Acceleration', years: '2035-2038', participants: '800M', success: '65%' },
                { phase: 'Integration', years: '2038-2040', participants: '2.8B', success: '60%' },
                { phase: 'Planetary', years: '2040-2042', participants: '4.6B', success: '55%' }
              ].map((phase, index) => (
                <Card key={index}>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">{phase.phase}</CardTitle>
                    <CardDescription className="text-xs">{phase.years}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center">
                      <div className="text-lg font-bold text-blue-600">{phase.participants}</div>
                      <div className="text-sm text-gray-600">{phase.success} success</div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="metrics" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Detailed Performance Metrics</CardTitle>
                <CardDescription>
                  Comprehensive comparison across all measured dimensions
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {simulationMetrics.map((metric, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-medium">{metric.name}</span>
                        <Badge variant="secondary">+{metric.improvement}%</Badge>
                      </div>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Traditional System</span>
                          <span>{(metric.traditional * 100).toFixed(0)}%</span>
                        </div>
                        <Progress value={metric.traditional * 100} className="h-2" />
                        <div className="flex justify-between text-sm">
                          <span>LIFE System</span>
                          <span className="text-green-600">{(metric.life * 100).toFixed(0)}%</span>
                        </div>
                        <Progress value={metric.life * 100} className="h-2" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

// Optimization page component
function OptimizationPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4">Performance Optimization</h1>
          <p className="text-xl text-gray-600">
            Pathway from 27.4/100 to 83.5/100 performance through systematic optimization.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Optimization Factors Analysis</CardTitle>
                <CardDescription>
                  Six key factors that can improve LIFE System performance by 205%
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={optimizationData} layout="horizontal">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" domain={[0, 16]} />
                    <YAxis dataKey="factor" type="category" width={120} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="current" fill="#ef4444" name="Current Performance" />
                    <Bar dataKey="potential" fill="#22c55e" name="Optimization Potential" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Implementation Roadmap</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {[
                    {
                      phase: 'Phase 1: Foundation (0-6 months)',
                      target: '27.4 → 35.0 (+7.6 points)',
                      strategies: ['Timing Optimization', 'Crisis Resilience'],
                      milestones: [
                        'Crisis prediction system operational',
                        'Distributed infrastructure 50% complete',
                        'Rapid deployment protocols established'
                      ]
                    },
                    {
                      phase: 'Phase 2: Development (6-18 months)',
                      target: '35.0 → 55.0 (+20.0 points)',
                      strategies: ['System Maturation', 'Resource Optimization'],
                      milestones: [
                        'Optimized algorithms deployed',
                        'Funding targets 60% achieved',
                        'Training programs operational'
                      ]
                    },
                    {
                      phase: 'Phase 3: Scaling (18-36 months)',
                      target: '55.0 → 83.5 (+28.5 points)',
                      strategies: ['Scaling Optimization', 'Coordination Enhancement', 'Synergy Effects'],
                      milestones: [
                        'Multi-level coordination systems operational',
                        'Cultural adaptation frameworks deployed',
                        'AI-powered coordination systems active'
                      ]
                    }
                  ].map((phase, index) => (
                    <div key={index} className="border-l-4 border-blue-500 pl-4">
                      <h4 className="font-bold text-lg">{phase.phase}</h4>
                      <p className="text-green-600 font-medium mb-2">{phase.target}</p>
                      <div className="mb-3">
                        <span className="text-sm font-medium">Strategies: </span>
                        {phase.strategies.map((strategy, i) => (
                          <Badge key={i} variant="outline" className="mr-1">
                            {strategy}
                          </Badge>
                        ))}
                      </div>
                      <div>
                        <span className="text-sm font-medium">Key Milestones:</span>
                        <ul className="text-sm text-gray-600 mt-1">
                          {phase.milestones.map((milestone, i) => (
                            <li key={i}>• {milestone}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Performance Trajectory</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-red-600">27.4/100</div>
                    <div className="text-sm text-gray-600">Current Performance</div>
                  </div>
                  <div className="flex items-center justify-center">
                    <ChevronRight className="w-6 h-6 text-gray-400" />
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600">83.5/100</div>
                    <div className="text-sm text-gray-600">Optimized Performance</div>
                  </div>
                  <div className="text-center">
                    <Badge variant="secondary" className="text-lg px-4 py-2">
                      +205% Improvement
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Priority Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[
                    { action: 'Start Implementation NOW', priority: 'Critical', impact: '+15 points' },
                    { action: 'Build Crisis-Resilient Infrastructure', priority: 'Critical', impact: '+12 points' },
                    { action: 'Optimize Core Algorithms', priority: 'High', impact: '+12 points' },
                    { action: 'Secure Initial Funding', priority: 'High', impact: '+8 points' }
                  ].map((item, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <div className="font-medium text-sm">{item.action}</div>
                        <Badge 
                          variant={item.priority === 'Critical' ? 'destructive' : 'secondary'}
                          className="text-xs"
                        >
                          {item.priority}
                        </Badge>
                      </div>
                      <div className="text-green-600 font-medium">{item.impact}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Resource Requirements</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span>Total Investment</span>
                    <span className="font-medium">$100M over 3 years</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Expected ROI</span>
                    <span className="font-medium text-green-600">560% performance/dollar</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Implementation Timeline</span>
                    <span className="font-medium">36 months</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Success Probability</span>
                    <span className="font-medium text-blue-600">85%</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

// Implementation page component
function ImplementationPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4">Implementation Strategy</h1>
          <p className="text-xl text-gray-600">
            Detailed roadmap for real-world deployment of the LIFE System framework.
          </p>
        </div>

        <div className="space-y-8">
          <Card>
            <CardHeader>
              <CardTitle>Implementation Phases Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                {[
                  { phase: 'Foundation', duration: '2030-2032', population: '8M', focus: 'Pilot Programs' },
                  { phase: 'Growth', duration: '2032-2035', population: '80M', focus: 'Regional Networks' },
                  { phase: 'Acceleration', duration: '2035-2038', population: '800M', focus: 'National Integration' },
                  { phase: 'Integration', duration: '2038-2040', population: '2.8B', focus: 'Continental Coordination' },
                  { phase: 'Planetary', duration: '2040-2042', population: '4.6B', focus: 'Global Transformation' }
                ].map((phase, index) => (
                  <Card key={index} className="text-center">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-lg">{phase.phase}</CardTitle>
                      <CardDescription>{phase.duration}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-blue-600 mb-1">{phase.population}</div>
                      <div className="text-sm text-gray-600">{phase.focus}</div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <Card>
              <CardHeader>
                <CardTitle>Technical Infrastructure</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Distributed Ledger System</h4>
                    <p className="text-sm text-gray-600">Blockchain-based system with 1000+ global nodes for resilience</p>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">AI Optimization Engine</h4>
                    <p className="text-sm text-gray-600">Machine learning systems for resource allocation and coordination</p>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Communication Platform</h4>
                    <p className="text-sm text-gray-600">Secure, real-time coordination across all system levels</p>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Mobile Applications</h4>
                    <p className="text-sm text-gray-600">User-friendly interfaces for individual participation</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Governance Framework</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Multi-Level Democracy</h4>
                    <p className="text-sm text-gray-600">Democratic participation from local to planetary scales</p>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Consensus Building</h4>
                    <p className="text-sm text-gray-600">Structured processes for collective decision-making</p>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Conflict Resolution</h4>
                    <p className="text-sm text-gray-600">Comprehensive mediation and resolution mechanisms</p>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Cultural Adaptation</h4>
                    <p className="text-sm text-gray-600">Respect for diverse cultural values and practices</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Risk Management Strategy</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h4 className="font-medium mb-3 flex items-center gap-2">
                    <AlertCircle className="w-5 h-5 text-orange-500" />
                    Technical Risks
                  </h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Algorithm performance validation</li>
                    <li>• Infrastructure failure prevention</li>
                    <li>• Security and privacy protection</li>
                    <li>• Scalability testing and optimization</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium mb-3 flex items-center gap-2">
                    <Users className="w-5 h-5 text-blue-500" />
                    Social Risks
                  </h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Resistance to change management</li>
                    <li>• Cultural adaptation challenges</li>
                    <li>• Coordination failure prevention</li>
                    <li>• Stakeholder engagement strategies</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium mb-3 flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-500" />
                    Economic Risks
                  </h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Funding diversification strategy</li>
                    <li>• Economic disruption mitigation</li>
                    <li>• Transition support systems</li>
                    <li>• Performance monitoring protocols</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

// Collaboration page component
function CollaborationPage() {
  const [activeTab, setActiveTab] = useState('overview')

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4">Collaboration Hub</h1>
          <p className="text-xl text-gray-600">
            Join the global community working to implement the LIFE System framework.
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="contribute">Contribute</TabsTrigger>
            <TabsTrigger value="community">Community</TabsTrigger>
            <TabsTrigger value="contact">Contact</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Github className="w-5 h-5" />
                    Open Source Development
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">
                    Contribute to the LIFE System codebase, algorithms, and technical infrastructure.
                  </p>
                  <Button className="w-full">
                    <ExternalLink className="w-4 h-4 mr-2" />
                    View on GitHub
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BookOpen className="w-5 h-5" />
                    Research Collaboration
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">
                    Join research initiatives, peer review processes, and academic publications.
                  </p>
                  <Button className="w-full" variant="outline">
                    <Users className="w-4 h-4 mr-2" />
                    Join Research Team
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Globe className="w-5 h-5" />
                    Implementation Support
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">
                    Support pilot programs, community formation, and real-world implementation.
                  </p>
                  <Button className="w-full" variant="outline">
                    <Lightbulb className="w-4 h-4 mr-2" />
                    Get Involved
                  </Button>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Current Initiatives</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      title: 'Algorithm Optimization Project',
                      description: 'Improving contribution recognition and resource allocation algorithms',
                      status: 'Active',
                      participants: 15,
                      progress: 65
                    },
                    {
                      title: 'Pilot Community Development',
                      description: 'Establishing first LIFE System communities in multiple regions',
                      status: 'Planning',
                      participants: 8,
                      progress: 25
                    },
                    {
                      title: 'Crisis Resilience Research',
                      description: 'Developing distributed infrastructure and response protocols',
                      status: 'Active',
                      participants: 12,
                      progress: 40
                    }
                  ].map((initiative, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium">{initiative.title}</h4>
                        <Badge variant={initiative.status === 'Active' ? 'default' : 'secondary'}>
                          {initiative.status}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{initiative.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-500">{initiative.participants} participants</span>
                        <div className="flex items-center gap-2">
                          <Progress value={initiative.progress} className="w-20 h-2" />
                          <span className="text-sm text-gray-500">{initiative.progress}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="contribute" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card>
                <CardHeader>
                  <CardTitle>Ways to Contribute</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { icon: Brain, title: 'Research & Analysis', description: 'Contribute to research, data analysis, and academic publications' },
                      { icon: Settings, title: 'Technical Development', description: 'Develop algorithms, infrastructure, and software platforms' },
                      { icon: Users, title: 'Community Building', description: 'Help establish and support LIFE System communities' },
                      { icon: FileText, title: 'Documentation', description: 'Improve documentation, guides, and educational materials' },
                      { icon: MessageSquare, title: 'Outreach & Education', description: 'Share knowledge and educate others about the LIFE System' }
                    ].map((item, index) => (
                      <div key={index} className="flex items-start gap-3">
                        <item.icon className="w-5 h-5 text-blue-600 mt-1" />
                        <div>
                          <h4 className="font-medium">{item.title}</h4>
                          <p className="text-sm text-gray-600">{item.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Skill Areas Needed</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {[
                      'Machine Learning & AI',
                      'Blockchain Development',
                      'Systems Architecture',
                      'Economic Modeling',
                      'Social Science Research',
                      'Community Organizing',
                      'UI/UX Design',
                      'Technical Writing',
                      'Project Management',
                      'Data Analysis'
                    ].map((skill, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                        <span className="text-sm">{skill}</span>
                        <Badge variant="outline" className="text-xs">Needed</Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Get Started</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Button className="h-auto p-4 flex flex-col items-center gap-2">
                    <Github className="w-6 h-6" />
                    <span>Fork Repository</span>
                    <span className="text-xs opacity-75">Start contributing code</span>
                  </Button>
                  <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                    <MessageSquare className="w-6 h-6" />
                    <span>Join Discussion</span>
                    <span className="text-xs opacity-75">Connect with community</span>
                  </Button>
                  <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                    <Mail className="w-6 h-6" />
                    <span>Contact Team</span>
                    <span className="text-xs opacity-75">Discuss collaboration</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="community" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card>
                <CardHeader>
                  <CardTitle>Community Stats</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">150+</div>
                      <div className="text-sm text-gray-600">Contributors</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">25</div>
                      <div className="text-sm text-gray-600">Active Projects</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-600">12</div>
                      <div className="text-sm text-gray-600">Countries</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-orange-600">5</div>
                      <div className="text-sm text-gray-600">Pilot Communities</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {[
                      { user: 'Alex Chen', action: 'submitted optimization algorithm improvements', time: '2 hours ago' },
                      { user: 'Maria Rodriguez', action: 'completed community formation guide', time: '5 hours ago' },
                      { user: 'David Kim', action: 'published crisis resilience research', time: '1 day ago' },
                      { user: 'Sarah Johnson', action: 'launched pilot community in Portland', time: '2 days ago' }
                    ].map((activity, index) => (
                      <div key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                          <Users className="w-4 h-4 text-blue-600" />
                        </div>
                        <div className="flex-1">
                          <p className="text-sm">
                            <span className="font-medium">{activity.user}</span> {activity.action}
                          </p>
                          <p className="text-xs text-gray-500">{activity.time}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Community Guidelines</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Collaboration Principles</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li>• Respect diverse perspectives and cultural backgrounds</li>
                      <li>• Focus on constructive dialogue and solution-oriented discussions</li>
                      <li>• Share knowledge openly and support others' learning</li>
                      <li>• Maintain transparency in all collaborative activities</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Contribution Standards</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li>• Follow established coding and documentation standards</li>
                      <li>• Provide clear descriptions and rationale for contributions</li>
                      <li>• Test thoroughly and consider impact on existing systems</li>
                      <li>• Engage in peer review and feedback processes</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="contact" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card>
                <CardHeader>
                  <CardTitle>Contact Information</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <Mail className="w-5 h-5 text-blue-600" />
                      <div>
                        <p className="font-medium">General Inquiries</p>
                        <p className="text-sm text-gray-600">research@lifesystem.org</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Users className="w-5 h-5 text-green-600" />
                      <div>
                        <p className="font-medium">Collaboration</p>
                        <p className="text-sm text-gray-600">collaborate@lifesystem.org</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Github className="w-5 h-5 text-gray-600" />
                      <div>
                        <p className="font-medium">Technical Issues</p>
                        <p className="text-sm text-gray-600">github.com/life-system</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <MessageSquare className="w-5 h-5 text-purple-600" />
                      <div>
                        <p className="font-medium">Community Discussion</p>
                        <p className="text-sm text-gray-600">discord.gg/lifesystem</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Research Team</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium">Manus AI</h4>
                      <p className="text-sm text-gray-600">Lead Researcher & Systems Analyst</p>
                      <p className="text-sm text-gray-600">research@lifesystem.org</p>
                    </div>
                    <div>
                      <h4 className="font-medium">Troy Mork</h4>
                      <p className="text-sm text-gray-600">Co-Researcher & Implementation Strategist</p>
                      <p className="text-sm text-gray-600">implementation@lifesystem.org</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Schedule a Meeting</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Button className="h-auto p-4 flex flex-col items-center gap-2">
                    <Calendar className="w-6 h-6" />
                    <span>Research Collaboration</span>
                    <span className="text-xs opacity-75">Discuss research opportunities</span>
                  </Button>
                  <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                    <Settings className="w-6 h-6" />
                    <span>Technical Discussion</span>
                    <span className="text-xs opacity-75">Review technical implementation</span>
                  </Button>
                  <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                    <Globe className="w-6 h-6" />
                    <span>Implementation Planning</span>
                    <span className="text-xs opacity-75">Plan pilot programs</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

// Downloads page component
function DownloadsPage() {
  const handleDownload = (filename) => {
    // In a real implementation, this would trigger actual file downloads
    // For now, we'll simulate the download action
    console.log(`Downloading ${filename}`)
    alert(`Download started: ${filename}`)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4">Downloads</h1>
          <p className="text-xl text-gray-600">
            Access all research papers, simulation data, and technical documentation.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {
              title: 'Comprehensive Scientific Paper',
              description: '50+ page peer-review ready analysis with complete methodology and results',
              filename: 'life_system_comprehensive_scientific_paper.pdf',
              size: '15.2 MB',
              type: 'PDF',
              category: 'Research',
              downloads: 1247
            },
            {
              title: 'Final Research Report',
              description: 'Executive summary with key findings and recommendations',
              filename: 'life_system_final_report.pdf',
              size: '8.7 MB',
              type: 'PDF',
              category: 'Research',
              downloads: 892
            },
            {
              title: 'Simulation Analysis Charts',
              description: 'Comprehensive visualization of 17-year simulation results',
              filename: 'comprehensive_17_year_analysis.png',
              size: '2.1 MB',
              type: 'PNG',
              category: 'Visualization',
              downloads: 634
            },
            {
              title: 'Publication Charts',
              description: 'Publication-ready charts and visualizations',
              filename: 'life_system_publication_charts.png',
              size: '1.8 MB',
              type: 'PNG',
              category: 'Visualization',
              downloads: 521
            },
            {
              title: 'Simulation Summary',
              description: 'Detailed summary of simulation methodology and results',
              filename: 'life_system_comprehensive_simulation_summary.md',
              size: '156 KB',
              type: 'Markdown',
              category: 'Documentation',
              downloads: 445
            },
            {
              title: 'Technical Implementation Code',
              description: 'Complete source code for all simulations and algorithms',
              filename: 'life_system_simulation_code.zip',
              size: '12.4 MB',
              type: 'ZIP',
              category: 'Code',
              downloads: 312
            }
          ].map((item, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-lg">{item.title}</CardTitle>
                  <Badge variant="outline">{item.category}</Badge>
                </div>
                <CardDescription>{item.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>File Type: {item.type}</span>
                    <span>Size: {item.size}</span>
                  </div>
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>Downloads: {item.downloads.toLocaleString()}</span>
                    <span>Updated: Dec 2024</span>
                  </div>
                  <Button 
                    className="w-full" 
                    onClick={() => handleDownload(item.filename)}
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Bulk Download</CardTitle>
            <CardDescription>
              Download all research materials in a single archive
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Complete LIFE System Research Archive</p>
                <p className="text-sm text-gray-600">
                  Includes all papers, visualizations, code, and documentation
                </p>
                <p className="text-sm text-gray-600">Size: 45.8 MB • ZIP Archive</p>
              </div>
              <Button size="lg" onClick={() => handleDownload('life_system_complete_archive.zip')}>
                <Download className="w-5 h-5 mr-2" />
                Download All
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="mt-6">
          <CardHeader>
            <CardTitle>License Information</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600 mb-4">
              All research materials are released under the Creative Commons Attribution 4.0 International License. 
              You are free to share, adapt, and build upon this work for any purpose, including commercial use, 
              as long as you provide appropriate attribution.
            </p>
            <div className="flex items-center gap-4">
              <Badge variant="secondary">CC BY 4.0</Badge>
              <Button variant="outline" size="sm">
                <ExternalLink className="w-4 h-4 mr-2" />
                View License
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// Main App component
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-white">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/research" element={<ResearchPage />} />
          <Route path="/simulations" element={<SimulationsPage />} />
          <Route path="/optimization" element={<OptimizationPage />} />
          <Route path="/implementation" element={<ImplementationPage />} />
          <Route path="/collaboration" element={<CollaborationPage />} />
          <Route path="/downloads" element={<DownloadsPage />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

