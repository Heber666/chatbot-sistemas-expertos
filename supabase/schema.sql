create extension if not exists "pgcrypto";

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text not null unique,
  full_name text,
  created_at timestamptz not null default now()
);

create table if not exists public.conversations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  title text not null default 'Nueva conversación',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null references public.conversations(id) on delete cascade,
  role text not null check (role in ('user', 'assistant')),
  content text not null,
  attachment jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.contexts (
  conversation_id uuid primary key references public.conversations(id) on delete cascade,
  document_fragments jsonb not null default '[]'::jsonb,
  document_names jsonb not null default '[]'::jsonb,
  audio_transcriptions text not null default '',
  audio_names jsonb not null default '[]'::jsonb,
  metadata jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now()
);

create index if not exists conversations_user_updated_idx
  on public.conversations(user_id, updated_at desc);
create index if not exists messages_conversation_created_idx
  on public.messages(conversation_id, created_at);

alter table public.profiles enable row level security;
alter table public.conversations enable row level security;
alter table public.messages enable row level security;
alter table public.contexts enable row level security;

create policy "Users can read their profile"
  on public.profiles for select using (auth.uid() = id);
create policy "Users can update their profile"
  on public.profiles for update using (auth.uid() = id);

create policy "Users can manage their conversations"
  on public.conversations for all using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "Users can manage messages in their conversations"
  on public.messages for all using (
    exists (
      select 1 from public.conversations
      where conversations.id = messages.conversation_id
        and conversations.user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from public.conversations
      where conversations.id = messages.conversation_id
        and conversations.user_id = auth.uid()
    )
  );

create policy "Users can manage their contexts"
  on public.contexts for all using (
    exists (
      select 1 from public.conversations
      where conversations.id = contexts.conversation_id
        and conversations.user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from public.conversations
      where conversations.id = contexts.conversation_id
        and conversations.user_id = auth.uid()
    )
  );

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  if lower(new.email) not like '%@unab.edu.sv' then
    raise exception 'Solo se permiten correos @unab.edu.sv';
  end if;
  insert into public.profiles (id, email, full_name)
  values (new.id, lower(new.email), new.raw_user_meta_data ->> 'full_name');
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
