'use client';

import cx from 'classnames';
import type React from 'react';
import {
  useRef,
  useEffect,
  useCallback,
  memo,
} from 'react';
import { useLocalStorage, useWindowSize } from 'usehooks-ts';

import { ArrowUpIcon } from './icons';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import type { UseChatHelpers } from '@ai-sdk/react';

function PureMultimodalInput({
  input,
  setInput,
  setMessages,
  className,
}: {
  input: string;
  setInput: (input: string) => void;
  setMessages: UseChatHelpers['setMessages']; 
  className?: string;
}) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { width } = useWindowSize();

  const [localStorageInput, setLocalStorageInput] = useLocalStorage(
    'input',
    '',
  );

  useEffect(() => {
    if (textareaRef.current) {
      const domValue = textareaRef.current.value;
      const finalValue = domValue || localStorageInput || '';
      setInput(finalValue);
    }
  }, []);

  useEffect(() => {
    setLocalStorageInput(input);
  }, [input, setLocalStorageInput]);

  const handleInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(event.target.value);
  };

  const submitForm = useCallback(async () => {
    if (input.trim()) {
      // Add user message
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: Date.now().toString(),
          role: 'user',
          content: input,
          createdAt: new Date()
        }
      ]);
      
      try {
        // Send message to the server
        const response = await fetch('api/chatbot/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: input,
          }),
        });

        if (!response.ok) {
          throw new Error('Could not fetch the answer.' + response.status);
        }
        
        const data = await response.json();
        const { message } = data;
        
        // Update messages with the response
        setMessages((currentMessages) => [
          ...currentMessages,
          {
            id: Date.now().toString(),
            role: 'assistant',
            content: message,
            createdAt: new Date()
          }
        ]);
      } catch (error) {
        console.error('Error communicating with chatbot:', error);
        setMessages((currentMessages) => [
          ...currentMessages,
          {
            id: Date.now().toString(),
            role: 'assistant',
            content: 'Sorry, there was an error processing your request.',
            createdAt: new Date()
          }
        ]);
      } finally {
        setLocalStorageInput('');
        setInput('');
        
        if (width && width > 768) {
          textareaRef.current?.focus();
        }
      }
    }
  }, [
    input,
    setInput,
    setMessages,
    setLocalStorageInput,
    width
  ]);

  return (
    <div className="relative w-full flex flex-col gap-4">

      <Textarea
        data-testid="multimodal-input"
        ref={textareaRef}
        placeholder="Send a message..."
        value={input}
        onChange={handleInput}
        className={cx(
          'h-12 overflow-auto resize-none rounded-2xl !text-base bg-muted pb-10 dark:border-zinc-700',
          className,
        )}
        rows={1}
        autoFocus
        onKeyDown={(event) => {
          if (
            event.key === 'Enter' &&
            !event.shiftKey &&
            !event.nativeEvent.isComposing
          ) {
            event.preventDefault();
            submitForm();
          }
        }}
      />

      <div className="absolute bottom-0 right-0 p-2 w-fit flex flex-row justify-end">
        <SendButton
          input={input}
          submitForm={submitForm}
        />
      </div>
    </div>
  );
}

export const MultimodalInput = memo(
  PureMultimodalInput,
  (prevProps, nextProps) => {
    return prevProps.input === nextProps.input;
  },
);

function PureSendButton({
  submitForm,
  input,
}: {
  submitForm: () => void;
  input: string;
}) {
  return (
    <Button
      data-testid="send-button"
      className="rounded-full p-1.5 h-fit border dark:border-zinc-600"
      onClick={(event) => {
        event.preventDefault();
        submitForm();
      }}
      disabled={input.length === 0}
    >
      <ArrowUpIcon size={14} />
    </Button>
  );
}

const SendButton = memo(PureSendButton, (prevProps, nextProps) => {
  return prevProps.input === nextProps.input;
});
