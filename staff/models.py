"""Staff-side models. Just the audit log for now.

Every privileged action an administrator takes (changing a role, deactivating
an account, adding a user, publishing content) is recorded here. On a
cyber-security platform, "who changed what, and when" is not a nice-to-have:
it is the difference between an incident you can investigate and one you can't.
Records are append-only in practice — nothing in the app edits or deletes them.
"""

from django.conf import settings
from django.db import models


class AdminAction(models.Model):
    """One privileged action by one administrator."""

    class Kind(models.TextChoices):
        ADD_USER = "add_user", "Added a user"
        ROLE_CHANGE = "role_change", "Changed a role"
        DEACTIVATE = "deactivate", "Deactivated an account"
        ACTIVATE = "activate", "Activated an account"
        RESEND_VERIFICATION = "resend_verification", "Resent verification"
        NUDGE = "nudge", "Sent a nudge"
        FLAG = "flag", "Flagged a learner"
        UNFLAG = "unflag", "Cleared a flag"
        PUBLISH = "publish", "Published content"
        UNPUBLISH = "unpublish", "Unpublished content"
        PUBLISH_LESSON = "publish_lesson", "Published a lesson"
        UNPUBLISH_LESSON = "unpublish_lesson", "Unpublished a lesson"
        EDIT_MODULE = "edit_module", "Edited a module"
        EDIT_LESSON = "edit_lesson", "Edited a lesson"
        EDIT_QUESTION = "edit_question", "Edited a quiz question"
        CREATE_ORG = "create_org", "Created an organisation"
        EDIT_ORG = "edit_org", "Edited an organisation"
        DELETE_ORG = "delete_org", "Deleted an organisation"
        ASSIGN_ORG = "assign_org", "Changed a learner's organisation"
        NOTE_ORG = "note_org", "Sent a note to an organisation"
        NOTE_USER = "note_user", "Sent a note to a learner"
        ADD_NOTE = "add_note", "Added a private note"
        RESET_QUIZ = "reset_quiz", "Reset a quiz attempt"
        RESET_PROGRESS = "reset_progress", "Reset course progress"
        BULK_ACTION = "bulk_action", "Ran a bulk action"
        BULK_INVITE = "bulk_invite", "Bulk-invited users"
        REVOKE_CERT = "revoke_cert", "Revoked a certificate"
        SET_DUE = "set_due", "Set a training due date"
        PASSWORD_RESET = "password_reset", "Sent a password reset"

    # SET_NULL, not CASCADE: deleting an admin account must never erase the
    # record of what they did. The trail outlives the actor.
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_actions",
    )
    action = models.CharField(max_length=32, choices=Kind.choices)
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_actions_received",
    )
    summary = models.CharField(
        max_length=255, help_text="A human-readable description of the action."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_actions"
        ordering = ["-created_at"]

    def __str__(self):
        return self.summary


class LearnerNote(models.Model):
    """A private, internal note an administrator keeps against a learner record.

    Distinct from the "send a note" action, which emails the learner. These are
    never shown to the learner: they are the admin's own running record of
    interactions (chased on 3 May, manager aware, on extended leave, etc.). The
    author is kept for accountability but SET_NULL so a removed admin does not
    erase the note.
    """

    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learner_notes",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authored_notes",
    )
    body = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "learner_notes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note on {self.learner_id} by {self.author_id}"
