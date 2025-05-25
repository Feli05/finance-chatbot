'use client';

import type { UIMessage } from 'ai';
import { AnimatePresence, motion } from 'framer-motion';
import { memo } from 'react';
import { AssistantIcon } from './icons';
import { MessageActions } from './message-actions';
import { cn } from '@/lib/utils';

const PurePreviewMessage = ({
  message,
  isLoading,
  isReadonly,
}: {
  message: UIMessage;
  isLoading: boolean;
  isReadonly: boolean;
}) => {
  return (
    <AnimatePresence>
      <motion.div
        data-testid={`message-${message.role}`}
        className="w-full mx-auto max-w-3xl px-4 group/message"
        initial={{ y: 5, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        data-role={message.role}
      >
        <div
          className={cn(
            'flex gap-4 w-full group-data-[role=user]/message:ml-auto group-data-[role=user]/message:max-w-2xl',
            {
              'group-data-[role=user]/message:w-fit': true,
            },
          )}
        >
          {message.role === 'assistant' && (
            <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border bg-background">
              <div className="translate-y-px">
                <AssistantIcon size={14} />
              </div>
            </div>
          )}

          <div className="flex flex-col gap-4 w-full">
            <div className="flex flex-row gap-2 items-start">
              <div
                data-testid="message-content"
                className={cn('flex flex-col gap-4', {
                  'bg-primary text-primary-foreground px-3 py-2 rounded-xl':
                    message.role === 'user',
                })}
              >
              {message.content}
              </div>
            </div>

            {!isReadonly && (
              <MessageActions
                key={`action-${message.id}`}
                message={message}
                isLoading={isLoading}
              />
            )}
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export const PreviewMessage = memo(
  PurePreviewMessage,
  (prevProps, nextProps) => {
    if (prevProps.isLoading !== nextProps.isLoading) return false;
    if (prevProps.message.id !== nextProps.message.id) return false;
    if (prevProps.message.content !== nextProps.message.content) return false;
    return true;
  },
);
