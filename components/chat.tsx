'use client';

import type { UIMessage } from 'ai';
import { useChat } from '@ai-sdk/react';
import { MultimodalInput } from './multimodal-input';
import { Messages } from './messages';
import { toast } from 'sonner';

export function Chat({
  initialMessages,
  isReadonly,
}: {
  initialMessages: Array<UIMessage>;
  isReadonly: boolean;
}) {

  const {
    messages,
    setMessages,
    handleSubmit,
    input,
    setInput,
    append,
    status,
    stop,
  } = useChat({
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

  return (
    <>
      <div className="flex flex-col min-w-0 h-dvh bg-background">

        <Messages
          status={status}
          messages={messages}
          isReadonly={isReadonly}
        />

        <form className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
          {!isReadonly && (
            <MultimodalInput
              input={input}
              setInput={setInput}
              handleSubmit={handleSubmit}
              status={status}
              stop={stop}
              setMessages={setMessages}
              append={append}
            />
          )}
        </form>
      </div>
    </>
  );
}
