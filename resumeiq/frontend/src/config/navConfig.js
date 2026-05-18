export const navConfig = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: '📊',
    type: 'item',
    alwaysEnabled: true
  },
  {
    id: 'resume-hub',
    label: 'Resume Hub',
    icon: '📂',
    type: 'group',
    items: [
      {
        id: 'resume',
        label: 'My Resume',
        icon: '📄',
        alwaysEnabled: true
      },
      {
        id: 'templates',
        label: 'Resume Templates',
        icon: '🎨'
      },
      {
        id: 'rewriter',
        label: 'Resume Rewriter',
        icon: '✏️'
      },
      {
        id: 'versioning',
        label: 'Resume Versioning',
        icon: '📌'
      },
      {
        id: 'compare',
        label: 'Resume Comparison',
        icon: '⚖️'
      }
    ]
  },
  {
    id: 'ai-analysis',
    label: 'AI Analysis',
    icon: '🧠',
    type: 'group',
    items: [
      {
        id: 'analyze',
        label: 'Resume Analyzer',
        icon: '📋'
      },
      {
        id: 'ats-score',
        label: 'ATS Score',
        icon: '⭐'
      },
      {
        id: 'keyword-optimizer',
        label: 'Keyword Optimizer',
        icon: '🔑'
      },
      {
        id: 'skill-gap',
        label: 'Skill Gap Analysis',
        icon: '🎓'
      }
    ]
  },
  {
    id: 'career-prep',
    label: 'Career Prep',
    icon: '🎯',
    type: 'group',
    items: [
      {
        id: 'matcher',
        label: 'Job Matcher',
        icon: '🔍'
      },
      {
        id: 'batch-match',
        label: 'Batch Job Matching',
        icon: '📊'
      },
      {
        id: 'cover-letter',
        label: 'Cover Letter',
        icon: '✍️'
      },
      {
        id: 'learning',
        label: 'Learning Path',
        icon: '📚'
      },
      {
        id: 'interview',
        label: 'Interview Coach',
        icon: '🎤'
      }
    ]
  },
  {
    id: 'career-toolkit',
    label: 'Career Toolkit',
    icon: '🚀',
    type: 'group',
    items: [
      {
        id: 'ai-career-copilot',
        label: 'AI Career Copilot',
        icon: '🤖'
      },
      {
        id: 'linkedin-optimizer',
        label: 'LinkedIn Optimizer',
        icon: '💼'
      },
      {
        id: 'star-responses',
        label: 'STAR Responses',
        icon: '⭐'
      },
      {
        id: 'email-templates',
        label: 'Email Templates',
        icon: '📧'
      },
      {
        id: 'portfolio-showcase',
        label: 'Portfolio Showcase',
        icon: '🎁'
      }
    ]
  },
  {
    id: 'achievements',
    label: 'Achievements',
    icon: '🏆',
    type: 'item',
    alwaysEnabled: true
  }
]

