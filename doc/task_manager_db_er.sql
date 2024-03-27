CREATE TABLE "user" (
  "id" integer PRIMARY KEY,
  "login" varchar
);

CREATE TABLE "task" (
  "id" integer PRIMARY KEY,
  "creator_id" integer,
  "name" varchar,
  "text" varchar
);

CREATE TABLE "comment" (
  "id" integer PRIMARY KEY,
  "task_id" integer,
  "commenter_id" integer,
  "to_comment" integer,
  "text" varchar
);

ALTER TABLE "task" ADD FOREIGN KEY ("creator_id") REFERENCES "user" ("id");

ALTER TABLE "comment" ADD FOREIGN KEY ("commenter_id") REFERENCES "user" ("id");

ALTER TABLE "comment" ADD FOREIGN KEY ("task_id") REFERENCES "task" ("id");
