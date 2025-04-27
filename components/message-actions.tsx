import type { Message } from 'ai';
import { useCopyToClipboard } from 'usehooks-ts';

import { CopyIcon } from './icons';
import { Button } from './ui/button';
import { memo } from 'react';
import { toast } from 'sonner';

export function PureMessageActions({
  message,
  isLoading,
}: {
  message: Message;
  isLoading: boolean;
}) {
  const [_, copyToClipboard] = useCopyToClipboard();

  if (isLoading) return null;
  if (message.role === 'user') return null;

  return (
    <div className="flex flex-row gap-2">
      <Button
        className="py-1 px-2 h-fit text-muted-foreground"
        variant="outline"
        onClick={async () => {
          if (!message.content) {
            toast.error("There's no text to copy!");
            return;
          }

          await copyToClipboard(message.content);
          toast.success('Copied to clipboard!');
        }}
      >
        <CopyIcon />
      </Button>
    </div>
  );
}

export const MessageActions = memo(
  PureMessageActions,
  (prevProps, nextProps) => {
    if (prevProps.isLoading !== nextProps.isLoading) return false;
    return true;
  },
);
