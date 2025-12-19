<!-- file: TODO.md -->
<!-- version: 1.0.0 -->
<!-- guid: 12345678-1234-1234-1234-123456789003 -->

# TODO - auto-module-tagging-action

## CI/CD Failures - HIGH PRIORITY

### #todo Fix YAML Line Length Errors
**Status:** Open
**Priority:** High
**Issue:** yamllint failing due to lines exceeding 80 character limit

**Error Messages:**
```
action.yml:6:81: [error] line too long (85 > 80 characters) (line-length)
action.yml:68:81: [error] line too long (94 > 80 characters) (line-length)
action.yml:108:81: [error] line too long (98 > 80 characters) (line-length)
action.yml:110:81: [error] line too long (118 > 80 characters) (line-length)
action.yml:142:81: [error] line too long (99 > 80 characters) (line-length)
action.yml:145:81: [error] line too long (119 > 80 characters) (line-length)
action.yml:183:81: [error] line too long (88 > 80 characters) (line-length)
action.yml:195:81: [error] line too long (90 > 80 characters) (line-length)
action.yml:196:81: [error] line too long (93 > 80 characters) (line-length)
action.yml:197:81: [error] line too long (86 > 80 characters) (line-length)
```

**Fix Required:**
- Break long lines in action.yml to comply with 80 character limit
- Focus on lines: 6, 68, 108, 110, 142, 145, 183, 195, 196, 197
- Use YAML multiline syntax for long descriptions or commands

**Files to Fix:**
- `action.yml` - All identified long lines

**Log File:** `/Users/jdfalk/repos/github.com/jdfalk/ghcommon/logs/ci-failures/auto-module-tagging-action_20251218_231445.log`

---

### #todo Fix Test Action Execution Error
**Status:** Open
**Priority:** High
**Issue:** Test action failing with exit code 128

**Error Message:**
```
##[warning]Restore cache failed: Dependencies file is not found
##[error]Process completed with exit code 128
```

**Root Cause:**
- Cache restore failing because go.sum not found
- Test execution failing (exit code 128 typically indicates git errors)
- May need proper Go module setup for testing

**Fix Required:**
- Investigate why test is failing with exit code 128
- Check if Go modules need to be initialized for testing
- Review test workflow to ensure proper setup

**Files to Check:**
- `.github/workflows/ci.yml` - Test job configuration
- Test scripts or commands being executed

---

## Migration Tasks

### #todo Migrate to Reusable Workflows
**Status:** Pending
**Priority:** Medium
**Dependencies:** CI failures must be fixed first

**Description:**
After fixing CI issues, migrate this action's workflow to use the new centralized reusable workflows from ghcommon:
- `.github/workflows/reusable-action-ci.yml`
- `.github/workflows/reusable-release.yml`

**Tasks:**
1. Fix yamllint errors (see above)
2. Fix test execution errors (see above)
3. Update workflow to call reusable workflow
4. Test that workflows still work correctly
5. Pull logs and verify success
6. Document any issues encountered

---

## Testing Requirements

### #todo Comprehensive Testing
**Status:** Pending
**Priority:** High

**Required Tests:**
1. Create test Go module structure
2. Test automatic tagging functionality
3. Test with monorepo scenarios
4. Test tag creation and pushing
5. Test with existing tags

**Test Coverage:**
- [ ] Single module tagging
- [ ] Multi-module monorepo tagging
- [ ] Semantic version increments
- [ ] Tag conflict handling
- [ ] Git operations (tag creation, push)

---

## Documentation Updates

### #todo Update Action Documentation
**Status:** Pending
**Priority:** Medium

**Required Updates:**
- Document CI fixes in changelog
- Update README with proper usage examples
- Document monorepo usage patterns
- Add troubleshooting section for common issues

---

**Last Updated:** 2025-12-19
**Next Review:** After CI fixes complete
