import React, { useState, useEffect, useRef } from 'react';
import { Search, MoreVertical, Send, Smile, Paperclip, Mic, Phone, Video, ArrowLeft, Check, CheckCheck, Camera, Settings, Users, MessageCircle, Bell, Lock, User, LogOut, X, Plus, Image, File, Volume2 } from 'lucide-react';

// Mock user data
const MOCK_USERS = [
  { id: 1, name: 'Alice Johnson', phone: '+1234567890', avatar: '👩', status: 'Hey there! I am using WhatsApp', online: true },
  { id: 2, name: 'Bob Smith', phone: '+1234567891', avatar: '👨', status: 'Busy', online: false },
  { id: 3, name: 'Carol White', phone: '+1234567892', avatar: '👩‍🦰', status: 'Available', online: true },
  { id: 4, name: 'David Brown', phone: '+1234567893', avatar: '👨‍🦱', status: 'At work', online: true },
  { id: 5, name: 'Emma Davis', phone: '+1234567894', avatar: '👩‍🦳', status: 'Sleeping', online: false },
];

const EMOJIS = ['😀', '😂', '😍', '😢', '😎', '👍', '❤️', '🎉', '🔥', '✨', '💯', '🙏'];

function WhatsAppClone() {
  const [currentUser, setCurrentUser] = useState(null);
  const [view, setView] = useState('login');
  const [chats, setChats] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [messages, setMessages] = useState({});
  const [messageInput, setMessageInput] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [typingUsers, setTypingUsers] = useState({});
  const [showNewChat, setShowNewChat] = useState(false);
  const [showNewGroup, setShowNewGroup] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [incomingCall, setIncomingCall] = useState(null);
  const [activeCall, setActiveCall] = useState(null);
  const [selectedGroupMembers, setSelectedGroupMembers] = useState([]);
  const [groupName, setGroupName] = useState('');
  const messagesEndRef = useRef(null);

  // Login/Signup
  const [authForm, setAuthForm] = useState({ email: '', password: '', phone: '', username: '' });

  useEffect(() => {
    if (selectedChat && messages[selectedChat.id]) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, selectedChat]);

  const handleLogin = () => {
    const user = {
      id: 'me',
      name: authForm.username || authForm.email.split('@')[0],
      phone: authForm.phone || '+1234567890',
      avatar: '👤',
      status: 'Hey there! I am using WhatsApp',
      online: true
    };
    setCurrentUser(user);
    setView('chat');
    
    // Initialize with some demo chats
    const demoChats = MOCK_USERS.slice(0, 3).map(u => ({
      id: u.id,
      name: u.name,
      avatar: u.avatar,
      lastMessage: 'Hey! How are you?',
      timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString(),
      unread: Math.floor(Math.random() * 5),
      online: u.online,
      type: 'direct'
    }));
    setChats(demoChats);
    
    // Initialize messages
    const initialMessages = {};
    demoChats.forEach(chat => {
      initialMessages[chat.id] = [
        {
          id: 1,
          sender: chat.id,
          text: 'Hey! How are you?',
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          status: 'read'
        }
      ];
    });
    setMessages(initialMessages);
  };

  const sendMessage = () => {
    if (!messageInput.trim() || !selectedChat) return;

    const newMessage = {
      id: Date.now(),
      sender: 'me',
      text: messageInput,
      timestamp: new Date().toISOString(),
      status: 'sent'
    };

    setMessages(prev => ({
      ...prev,
      [selectedChat.id]: [...(prev[selectedChat.id] || []), newMessage]
    }));

    setChats(prev => prev.map(chat => 
      chat.id === selectedChat.id 
        ? { ...chat, lastMessage: messageInput, timestamp: new Date().toISOString() }
        : chat
    ));

    setMessageInput('');
    setShowEmojiPicker(false);

    // Simulate delivery and read status
    setTimeout(() => {
      setMessages(prev => ({
        ...prev,
        [selectedChat.id]: prev[selectedChat.id].map(msg =>
          msg.id === newMessage.id ? { ...msg, status: 'delivered' } : msg
        )
      }));
    }, 1000);

    setTimeout(() => {
      setMessages(prev => ({
        ...prev,
        [selectedChat.id]: prev[selectedChat.id].map(msg =>
          msg.id === newMessage.id ? { ...msg, status: 'read' } : msg
        )
      }));
    }, 2000);

    // Simulate typing and response
    if (selectedChat.type === 'direct') {
      setTypingUsers(prev => ({ ...prev, [selectedChat.id]: true }));
      setTimeout(() => {
        setTypingUsers(prev => ({ ...prev, [selectedChat.id]: false }));
        const responses = [
          "That's great! 😊",
          "I see, tell me more!",
          "Interesting! 🤔",
          "Haha, awesome! 😂",
          "Sure thing!",
        ];
        const response = {
          id: Date.now() + 1,
          sender: selectedChat.id,
          text: responses[Math.floor(Math.random() * responses.length)],
          timestamp: new Date().toISOString(),
          status: 'read'
        };
        setMessages(prev => ({
          ...prev,
          [selectedChat.id]: [...(prev[selectedChat.id] || []), response]
        }));
        setChats(prev => prev.map(chat => 
          chat.id === selectedChat.id 
            ? { ...chat, lastMessage: response.text, timestamp: new Date().toISOString(), unread: chat.unread + 1 }
            : chat
        ));
      }, 3000);
    }
  };

  const startNewChat = (user) => {
    const existingChat = chats.find(c => c.id === user.id && c.type === 'direct');
    if (existingChat) {
      setSelectedChat(existingChat);
      setShowNewChat(false);
      return;
    }

    const newChat = {
      id: user.id,
      name: user.name,
      avatar: user.avatar,
      lastMessage: '',
      timestamp: new Date().toISOString(),
      unread: 0,
      online: user.online,
      type: 'direct'
    };
    setChats(prev => [newChat, ...prev]);
    setMessages(prev => ({ ...prev, [user.id]: [] }));
    setSelectedChat(newChat);
    setShowNewChat(false);
  };

  const createGroup = () => {
    if (!groupName.trim() || selectedGroupMembers.length < 2) return;

    const newGroup = {
      id: `group-${Date.now()}`,
      name: groupName,
      avatar: '👥',
      lastMessage: 'Group created',
      timestamp: new Date().toISOString(),
      unread: 0,
      type: 'group',
      members: selectedGroupMembers
    };

    setChats(prev => [newGroup, ...prev]);
    setMessages(prev => ({ 
      ...prev, 
      [newGroup.id]: [{
        id: 1,
        sender: 'system',
        text: `Group "${groupName}" created`,
        timestamp: new Date().toISOString(),
        status: 'read'
      }]
    }));
    setSelectedChat(newGroup);
    setShowNewGroup(false);
    setGroupName('');
    setSelectedGroupMembers([]);
  };

  const startCall = (isVideo) => {
    if (!selectedChat) return;
    setActiveCall({
      type: isVideo ? 'video' : 'voice',
      contact: selectedChat,
      duration: 0,
      muted: false,
      videoOff: false
    });
  };

  const simulateIncomingCall = () => {
    const randomUser = MOCK_USERS[Math.floor(Math.random() * MOCK_USERS.length)];
    setIncomingCall({
      type: Math.random() > 0.5 ? 'video' : 'voice',
      contact: randomUser
    });
  };

  const answerCall = () => {
    setActiveCall({
      ...incomingCall,
      duration: 0,
      muted: false,
      videoOff: false
    });
    setIncomingCall(null);
  };

  const endCall = () => {
    setActiveCall(null);
    setIncomingCall(null);
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 86400000) {
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    } else if (diff < 604800000) {
      return date.toLocaleDateString('en-US', { weekday: 'short' });
    }
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const filteredChats = chats.filter(chat =>
    chat.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Login Screen
  if (view === 'login') {
    return (
      <div className="h-screen bg-gray-900 flex items-center justify-center">
        <div className="bg-gray-800 p-8 rounded-lg shadow-2xl w-96">
          <div className="text-center mb-6">
            <div className="mx-auto mb-4 w-20 h-20 relative">
              <svg viewBox="0 0 100 100" className="w-full h-full">
                <path
                  d="M50 10 L35 40 L50 40 L40 70 L70 45 L55 45 L65 20 Z"
                  fill="#10b981"
                  stroke="#10b981"
                  strokeWidth="2"
                />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Talk To Connect</h1>
            <p className="text-gray-400">Sign in to continue</p>
          </div>
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Username"
              value={authForm.username}
              onChange={(e) => setAuthForm({ ...authForm, username: e.target.value })}
              className="w-full bg-gray-700 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <input
              type="email"
              placeholder="Email"
              value={authForm.email}
              onChange={(e) => setAuthForm({ ...authForm, email: e.target.value })}
              className="w-full bg-gray-700 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <input
              type="tel"
              placeholder="Phone Number"
              value={authForm.phone}
              onChange={(e) => setAuthForm({ ...authForm, phone: e.target.value })}
              className="w-full bg-gray-700 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <input
              type="password"
              placeholder="Password"
              value={authForm.password}
              onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
              className="w-full bg-gray-700 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <button
              onClick={handleLogin}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold transition"
            >
              Sign In
            </button>
            <p className="text-center text-gray-400 text-sm">
              Don't have an account? Just sign in to create one!
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Incoming Call Screen
  if (incomingCall) {
    return (
      <div className="h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-8xl mb-6">{incomingCall.contact.avatar}</div>
          <h2 className="text-3xl text-white font-semibold mb-2">{incomingCall.contact.name}</h2>
          <p className="text-gray-400 mb-8">
            {incomingCall.type === 'video' ? 'Video' : 'Voice'} Call
          </p>
          <div className="flex gap-8 justify-center">
            <button
              onClick={endCall}
              className="bg-red-600 hover:bg-red-700 text-white p-6 rounded-full transition"
            >
              <X className="w-8 h-8" />
            </button>
            <button
              onClick={answerCall}
              className="bg-green-600 hover:bg-green-700 text-white p-6 rounded-full transition animate-pulse"
            >
              <Phone className="w-8 h-8" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Active Call Screen
  if (activeCall) {
    return (
      <div className="h-screen bg-gray-900 flex flex-col items-center justify-between py-12">
        <div className="text-center">
          <div className="text-8xl mb-6">{activeCall.contact.avatar}</div>
          <h2 className="text-3xl text-white font-semibold mb-2">{activeCall.contact.name}</h2>
          <p className="text-gray-400">
            {Math.floor(activeCall.duration / 60)}:{(activeCall.duration % 60).toString().padStart(2, '0')}
          </p>
        </div>
        
        {activeCall.type === 'video' && (
          <div className="bg-gray-800 rounded-lg p-4 w-48 h-36">
            <div className="w-full h-full bg-gray-700 rounded flex items-center justify-center">
              <Camera className="w-12 h-12 text-gray-500" />
            </div>
          </div>
        )}

        <div className="flex gap-6">
          <button
            onClick={() => setActiveCall({ ...activeCall, muted: !activeCall.muted })}
            className={`${activeCall.muted ? 'bg-red-600' : 'bg-gray-700'} hover:bg-gray-600 text-white p-4 rounded-full transition`}
          >
            <Mic className="w-6 h-6" />
          </button>
          {activeCall.type === 'video' && (
            <button
              onClick={() => setActiveCall({ ...activeCall, videoOff: !activeCall.videoOff })}
              className={`${activeCall.videoOff ? 'bg-red-600' : 'bg-gray-700'} hover:bg-gray-600 text-white p-4 rounded-full transition`}
            >
              <Video className="w-6 h-6" />
            </button>
          )}
          <button
            className="bg-gray-700 hover:bg-gray-600 text-white p-4 rounded-full transition"
          >
            <Volume2 className="w-6 h-6" />
          </button>
          <button
            onClick={endCall}
            className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-full transition"
          >
            <Phone className="w-6 h-6 rotate-135" />
          </button>
        </div>
      </div>
    );
  }

  // Profile Screen
  if (showProfile) {
    return (
      <div className="h-screen bg-gray-900">
        <div className="bg-gray-800 p-4 flex items-center gap-4">
          <button onClick={() => setShowProfile(false)} className="text-white">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h2 className="text-white text-xl font-semibold">Profile</h2>
        </div>
        <div className="p-6">
          <div className="text-center mb-8">
            <div className="text-8xl mb-4">{currentUser?.avatar}</div>
            <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition">
              Change Photo
            </button>
          </div>
          <div className="space-y-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <label className="text-gray-400 text-sm">Name</label>
              <input
                type="text"
                value={currentUser?.name}
                className="w-full bg-transparent text-white text-lg outline-none"
              />
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <label className="text-gray-400 text-sm">About</label>
              <input
                type="text"
                value={currentUser?.status}
                className="w-full bg-transparent text-white text-lg outline-none"
              />
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <label className="text-gray-400 text-sm">Phone</label>
              <p className="text-white text-lg">{currentUser?.phone}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Settings Screen
  if (showSettings) {
    return (
      <div className="h-screen bg-gray-900">
        <div className="bg-gray-800 p-4 flex items-center gap-4">
          <button onClick={() => setShowSettings(false)} className="text-white">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h2 className="text-white text-xl font-semibold">Settings</h2>
        </div>
        <div className="divide-y divide-gray-700">
          <button className="w-full bg-gray-800 hover:bg-gray-700 p-4 flex items-center gap-4 transition">
            <Bell className="w-6 h-6 text-gray-400" />
            <span className="text-white">Notifications</span>
          </button>
          <button className="w-full bg-gray-800 hover:bg-gray-700 p-4 flex items-center gap-4 transition">
            <Lock className="w-6 h-6 text-gray-400" />
            <span className="text-white">Privacy</span>
          </button>
          <button className="w-full bg-gray-800 hover:bg-gray-700 p-4 flex items-center gap-4 transition">
            <User className="w-6 h-6 text-gray-400" />
            <span className="text-white">Account</span>
          </button>
          <button
            onClick={() => {
              setCurrentUser(null);
              setView('login');
            }}
            className="w-full bg-gray-800 hover:bg-gray-700 p-4 flex items-center gap-4 transition"
          >
            <LogOut className="w-6 h-6 text-red-500" />
            <span className="text-red-500">Logout</span>
          </button>
        </div>
      </div>
    );
  }

  // New Chat Modal
  if (showNewChat) {
    return (
      <div className="h-screen bg-gray-900">
        <div className="bg-gray-800 p-4 flex items-center gap-4">
          <button onClick={() => setShowNewChat(false)} className="text-white">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h2 className="text-white text-xl font-semibold">New Chat</h2>
        </div>
        <div className="p-4">
          <input
            type="text"
            placeholder="Search contacts..."
            className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>
        <div className="divide-y divide-gray-700">
          {MOCK_USERS.map(user => (
            <button
              key={user.id}
              onClick={() => startNewChat(user)}
              className="w-full bg-gray-800 hover:bg-gray-700 p-4 flex items-center gap-4 transition"
            >
              <div className="text-4xl">{user.avatar}</div>
              <div className="flex-1 text-left">
                <p className="text-white font-semibold">{user.name}</p>
                <p className="text-gray-400 text-sm">{user.status}</p>
              </div>
              {user.online && (
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              )}
            </button>
          ))}
        </div>
      </div>
    );
  }

  // New Group Modal
  if (showNewGroup) {
    return (
      <div className="h-screen bg-gray-900">
        <div className="bg-gray-800 p-4 flex items-center gap-4">
          <button onClick={() => setShowNewGroup(false)} className="text-white">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h2 className="text-white text-xl font-semibold">New Group</h2>
        </div>
        <div className="p-4 space-y-4">
          <input
            type="text"
            placeholder="Group name"
            value={groupName}
            onChange={(e) => setGroupName(e.target.value)}
            className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <p className="text-gray-400 text-sm">Select at least 2 members</p>
        </div>
        <div className="divide-y divide-gray-700">
          {MOCK_USERS.map(user => (
            <button
              key={user.id}
              onClick={() => {
                setSelectedGroupMembers(prev =>
                  prev.includes(user.id)
                    ? prev.filter(id => id !== user.id)
                    : [...prev, user.id]
                );
              }}
              className="w-full bg-gray-800 hover:bg-gray-700 p-4 flex items-center gap-4 transition"
            >
              <div className="text-4xl">{user.avatar}</div>
              <div className="flex-1 text-left">
                <p className="text-white font-semibold">{user.name}</p>
              </div>
              {selectedGroupMembers.includes(user.id) && (
                <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                  <Check className="w-4 h-4 text-white" />
                </div>
              )}
            </button>
          ))}
        </div>
        {selectedGroupMembers.length >= 2 && (
          <div className="fixed bottom-0 left-0 right-0 p-4 bg-gray-900">
            <button
              onClick={createGroup}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-full font-semibold transition"
            >
              Create Group
            </button>
          </div>
        )}
      </div>
    );
  }

  // Main Chat Interface
  return (
    <div className="h-screen bg-gray-900 flex">
      {/* Sidebar */}
      <div className="w-96 bg-gray-800 flex flex-col border-r border-gray-700">
        {/* Header */}
        <div className="bg-gray-900 p-4 flex items-center justify-between">
          <button onClick={() => setShowProfile(true)} className="text-4xl">
            {currentUser?.avatar}
          </button>
          <div className="flex gap-4">
            <button onClick={() => setShowNewChat(true)} className="text-gray-400 hover:text-white transition">
              <MessageCircle className="w-6 h-6" />
            </button>
            <button onClick={() => setShowNewGroup(true)} className="text-gray-400 hover:text-white transition">
              <Users className="w-6 h-6" />
            </button>
            <button onClick={() => setShowSettings(true)} className="text-gray-400 hover:text-white transition">
              <MoreVertical className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Search */}
        <div className="p-2 bg-gray-900">
          <div className="bg-gray-800 rounded-lg flex items-center px-4 py-2">
            <Search className="w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search or start new chat"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 bg-transparent text-white px-3 outline-none"
            />
          </div>
        </div>

        {/* Chat List */}
        <div className="flex-1 overflow-y-auto">
          {filteredChats.map(chat => (
            <button
              key={chat.id}
              onClick={() => {
                setSelectedChat(chat);
                setChats(prev => prev.map(c => 
                  c.id === chat.id ? { ...c, unread: 0 } : c
                ));
              }}
              className={`w-full p-4 flex items-center gap-4 hover:bg-gray-700 transition ${
                selectedChat?.id === chat.id ? 'bg-gray-700' : ''
              }`}
            >
              <div className="relative">
                <div className="text-4xl">{chat.avatar}</div>
                {chat.online && chat.type === 'direct' && (
                  <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-gray-800"></div>
                )}
              </div>
              <div className="flex-1 text-left">
                <div className="flex items-center justify-between mb-1">
                  <p className="text-white font-semibold">{chat.name}</p>
                  <span className="text-gray-400 text-xs">
                    {formatTime(chat.timestamp)}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <p className="text-gray-400 text-sm truncate">
                    {chat.lastMessage}
                  </p>
                  {chat.unread > 0 && (
                    <span className="bg-green-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {chat.unread}
                    </span>
                  )}
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {selectedChat ? (
          <>
            {/* Chat Header */}
            <div className="bg-gray-800 p-4 flex items-center justify-between border-b border-gray-700">
              <div className="flex items-center gap-4">
                <div className="relative">
                  <div className="text-4xl">{selectedChat.avatar}</div>
                  {selectedChat.online && selectedChat.type === 'direct' && (
                    <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-gray-800"></div>
                  )}
                </div>
                <div>
                  <p className="text-white font-semibold">{selectedChat.name}</p>
                  {typingUsers[selectedChat.id] ? (
                    <p className="text-green-500 text-sm">typing...</p>
                  ) : selectedChat.type === 'group' ? (
                    <p className="text-gray-400 text-sm">
                      {selectedChat.members?.length || 0} members
                    </p>
                  ) : (
                    <p className="text-gray-400 text-sm">
                      {selectedChat.online ? 'online' : 'offline'}
                    </p>
                  )}
                </div>
              </div>
              <div className="flex gap-4">
                <button
                  onClick={() => startCall(false)}
                  className="text-gray-400 hover:text-white transition"
                >
                  <Phone className="w-6 h-6" />
                </button>
                <button
                  onClick={() => startCall(true)}
                  className="text-gray-400 hover:text-white transition"
                >
                  <Video className="w-6 h-6" />
                </button>
                <button className="text-gray-400 hover:text-white transition">
                  <Search className="w-6 h-6" />
                </button>
                <button className="text-gray-400 hover:text-white transition">
                  <MoreVertical className="w-6 h-6" />
                </button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48cGF0dGVybiBpZD0iYSIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIj48cGF0aCBkPSJNMCAwaDQwdjQwSDB6IiBmaWxsPSIjMWYyOTM3Ii8+PHBhdGggZD0iTTAgMGg0MHY0MEgweiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMjkzZDRjIiBzdHJva2Utd2lkdGg9Ii41Ii8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2EpIi8+PC9zdmc+')]">
              {(messages[selectedChat.id] || []).map(msg => (
                <div
                  key={msg.id}
                  className={`flex ${msg.sender === 'me' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-md px-4 py-2 rounded-lg ${
                      msg.sender === 'me'
                        ? 'bg-green-700 text-white'
                        : msg.sender === 'system'
                        ? 'bg-gray-700 text-gray-300 text-center text-sm'
                        : 'bg-gray-800 text-white'
                    }`}
                  >
                    {selectedChat.type === 'group' && msg.sender !== 'me' && msg.sender !== 'system' && (
                      <p className="text-green-400 text-sm font-semibold mb-1">
                        {MOCK_USERS.find(u => u.id === msg.sender)?.name}
                      </p>
                    )}
                    <p>{msg.text}</p>
                    <div className="flex items-center justify-end gap-1 mt-1">
                      <span className="text-xs opacity-70">
                        {formatTime(msg.timestamp)}
                      </span>
                      {msg.sender === 'me' && (
                        <span>
                          {msg.status === 'sent' && <Check className="w-4 h-4" />}
                          {msg.status === 'delivered' && <CheckCheck className="w-4 h-4" />}
                          {msg.status === 'read' && <CheckCheck className="w-4 h-4 text-blue-400" />}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="bg-gray-800 p-4 flex items-center gap-4">
              <button
                onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                className="text-gray-400 hover:text-white transition"
              >
                <Smile className="w-6 h-6" />
              </button>
              <button className="text-gray-400 hover:text-white transition">
                <Paperclip className="w-6 h-6" />
              </button>
              
              {showEmojiPicker && (
                <div className="absolute bottom-20 left-4 bg-gray-700 rounded-lg p-4 shadow-xl">
                  <div className="grid grid-cols-6 gap-2">
                    {EMOJIS.map(emoji => (
                      <button
                        key={emoji}
                        onClick={() => {
                          setMessageInput(prev => prev + emoji);
                          setShowEmojiPicker(false);
                        }}
                        className="text-2xl hover:bg-gray-600 p-2 rounded transition"
                      >
                        {emoji}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              
              <input
                type="text"
                placeholder="Type a message"
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                className="flex-1 bg-gray-700 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-green-500"
              />
              
              {messageInput.trim() ? (
                <button
                  onClick={sendMessage}
                  className="bg-green-600 hover:bg-green-700 text-white p-3 rounded-full transition"
                >
                  <Send className="w-5 h-5" />
                </button>
              ) : (
                <button className="text-gray-400 hover:text-white transition p-3">
                  <Mic className="w-5 h-5" />
                </button>
              )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center bg-gray-900">
            <div className="mb-6">
              <svg viewBox="0 0 100 100" className="w-32 h-32">
                <path
                  d="M50 10 L35 40 L50 40 L40 70 L70 45 L55 45 L65 20 Z"
                  fill="#374151"
                  stroke="#374151"
                  strokeWidth="2"
                />
              </svg>
            </div>
            <h2 className="text-2xl text-gray-500 font-semibold mb-2">Talk To Connect</h2>
            <p className="text-gray-600">Select a chat to start messaging</p>
            <button
              onClick={simulateIncomingCall}
              className="mt-8 bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg transition"
            >
              Simulate Incoming Call
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default WhatsAppClone;
