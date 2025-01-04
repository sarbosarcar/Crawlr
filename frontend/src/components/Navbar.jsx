import { Disclosure } from '@headlessui/react'
import { useState, useEffect } from 'react'

const navigation = [
  { name: 'Home', href: '#', current: false },
  { name: 'Query', href: '#', current: true },
  { name: 'Contact', href: '#', current: false },
]

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Navbar() {
  const [isDarkMode, setIsDarkMode] = useState(true)

  // Update the class on the `html` element
  useEffect(() => {
    const root = window.document.documentElement
    if (isDarkMode) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  }, [isDarkMode])

  return (
    <Disclosure as="nav" className="bg-gray-600 dark:bg-gray-600 rounded-lg">
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="relative flex h-16 items-center justify-between">
          <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
            <div className="flex shrink-0 items-center">
              <p className="text-white font-bold text-2xl">Crawlr</p>
            </div>
            <div className="hidden sm:ml-6 sm:block">
              <div className="flex space-x-4">
                {navigation.map((item) => (
                  <a
                    key={item.name}
                    href={item.href}
                    aria-current={item.current ? 'page' : undefined}
                    className={classNames(
                      item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white',
                      'rounded-md px-3 py-2 text-sm font-medium',
                    )}
                  >
                    {item.name}
                  </a>
                ))}
              </div>
            </div>
          </div>
          <div className="flex items-center">
            {/* Toggle Button */}
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              className="bg-gray-900 text-black-800 dark:text-black-200 px-4 py-2 text-sm font-medium hover:bg-gray-700 rounded-lg"
            >
              {isDarkMode ? '☀️' : '🌙'}
            </button>
          </div>
        </div>
      </div>
    </Disclosure>
  )
}
