// Retired. This module used to read every page of the admin users list so the
// cohort member picker could search it in the browser and the roster could
// look up ID numbers. GET /api/admin/users now has a `search` parameter and the
// roster rows carry `id_no`, so nothing imports this file and it can be deleted.
export {};
