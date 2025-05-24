'use client';

import type { UIMessage } from 'ai';
import { useChat } from '@ai-sdk/react';
import { MultimodalInput } from './multimodal-input';
import { Messages } from './messages';
import { toast } from 'sonner';
import { Button } from './ui/button';
import { useState, useEffect } from 'react';

export function Chat({
  initialMessages,
  isReadonly,
}: {
  initialMessages: Array<UIMessage>;
  isReadonly: boolean;
}) {
  const [hasExited, setHasExited] = useState(false);
  const [key, setKey] = useState(Date.now()); 

  const {
    messages,
    setMessages,
    input,
    setInput,
    status,
    reload
  } = useChat({
    key: `chat-${key}`, 
    initialMessages,
    experimental_throttle: 100,
    sendExtraMessageFields: true,
    experimental_prepareRequestBody: (body) => ({
      message: body.messages.at(-1)
    }),
    onError: (error) => {
      toast.error(error.message);
    },
  });

  useEffect(() => {
    if (messages.length > 0 && !hasExited) {
      const lastMessage = messages[messages.length - 1];
      if (
        lastMessage.role === 'assistant' && 
        lastMessage.content.startsWith('Thank you for choosing us as your financial adviser')
      ) {
        setHasExited(true);
      }
    }
  }, [messages, hasExited]);

  // Reset chat to start a new conversation
  const handleNewChat = () => {
    setKey(Date.now());
    setMessages([]);
    setInput('');
    setHasExited(false);
    reload();
  };

  return (
    <>
      <div className="flex flex-col min-w-0 h-dvh bg-background relative">
        <div className="absolute top-2 right-2 z-10">
          <Button 
            onClick={handleNewChat}
            variant="outline" 
            size="sm"
            className="text-sm"
          >
            New Chat
          </Button>
        </div>

        <Messages
          status={status}
          messages={hasExited ? [] : messages}
          isReadonly={isReadonly}
          isExited={hasExited}
        />

        <form className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
          {!isReadonly && (
            <MultimodalInput
              input={input}
              setInput={setInput}
              setMessages={setMessages}
            />
          )}
        </form>
      </div>
    </>
  );
}
