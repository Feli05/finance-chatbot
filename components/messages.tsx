import type { UIMessage } from 'ai';
import { PreviewMessage } from './message';
import { useScrollToBottom } from './use-scroll-to-bottom';
import { Greeting } from './greeting';
import { memo, useState, useEffect } from 'react';
import equal from 'fast-deep-equal';
import type { UseChatHelpers } from '@ai-sdk/react';

interface MessagesProps {
  status: UseChatHelpers['status'];
  messages: Array<UIMessage>;
  isReadonly: boolean;
  isExited?: boolean;
}

function PureMessages({
  status,
  messages,
  isReadonly,
  isExited = false
}: MessagesProps) {
  const [messagesContainerRef, messagesEndRef] =
    useScrollToBottom<HTMLDivElement>();
  
  return (
    <div
      ref={messagesContainerRef}
      className="flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-4"
    >
      {messages.length === 0 && !isExited && <Greeting />}
      
      {isExited && (
        <Greeting 
          title="Chat Ended" 
          message="Click 'New Chat' to start another conversation." 
        />
      )}

      {messages.map((message, index) => (
        <PreviewMessage
          key={message.id}
          message={message}
          isLoading={status === 'streaming' && messages.length - 1 === index}
          isReadonly={isReadonly}
        />
      ))}

      <div
        ref={messagesEndRef}
        className="shrink-0 min-w-[24px] min-h-[24px]"
      />
    </div>
  );
}

export const Messages = memo(PureMessages, (prevProps, nextProps) => {
  if (prevProps.status !== nextProps.status) return false;
  if (prevProps.isReadonly !== nextProps.isReadonly) return false;
  if (prevProps.messages.length !== nextProps.messages.length) return false;
  if (prevProps.isExited !== nextProps.isExited) return false;

  return equal(prevProps.messages, nextProps.messages);
});